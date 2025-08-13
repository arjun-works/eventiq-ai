"""
Budget API Endpoints

This module handles budget management including expense tracking,
budget allocation, and financial reporting for events.
"""

from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import get_current_user, get_current_active_user
from app.models.user import User
from app.models.budget import Budget, BudgetCategory, Expense, ExpenseStatus

router = APIRouter()

# Pydantic schemas for request/response
class BudgetCreate(BaseModel):
    event_name: str
    total_budget: Decimal
    description: Optional[str] = None

class BudgetUpdate(BaseModel):
    total_budget: Optional[Decimal] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class BudgetResponse(BaseModel):
    id: int
    event_name: str
    total_budget: Decimal
    allocated_amount: Decimal
    spent_amount: Decimal
    remaining_amount: Decimal
    description: Optional[str]
    created_by: int
    created_at: datetime
    updated_at: datetime
    is_active: bool
    
    # Creator details
    creator_name: str

class CategoryCreate(BaseModel):
    budget_id: int
    name: str
    allocated_amount: Decimal
    description: Optional[str] = None

class CategoryUpdate(BaseModel):
    allocated_amount: Optional[Decimal] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class CategoryResponse(BaseModel):
    id: int
    budget_id: int
    name: str
    allocated_amount: Decimal
    spent_amount: Decimal
    remaining_amount: Decimal
    description: Optional[str]
    created_at: datetime
    is_active: bool

class ExpenseCreate(BaseModel):
    category_id: int
    vendor_name: str
    description: str
    amount: Decimal
    receipt_url: Optional[str] = None
    notes: Optional[str] = None

class ExpenseUpdate(BaseModel):
    vendor_name: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[Decimal] = None
    receipt_url: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[ExpenseStatus] = None

class ExpenseResponse(BaseModel):
    id: int
    category_id: int
    vendor_name: str
    description: str
    amount: Decimal
    receipt_url: Optional[str]
    notes: Optional[str]
    status: ExpenseStatus
    submitted_by: int
    submitted_at: datetime
    approved_by: Optional[int]
    approved_at: Optional[datetime]
    
    # Category and submitter details
    category_name: str
    submitter_name: str
    approver_name: Optional[str]


@router.post("/", response_model=BudgetResponse)
async def create_budget(
    budget_data: BudgetCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> BudgetResponse:
    """
    Create a new budget (admin/organizer only)
    """
    if current_user.role not in ["admin", "organizer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Check if budget already exists for this event
    result = await db.execute(
        select(Budget).where(Budget.event_name == budget_data.event_name)
    )
    existing_budget = result.scalar_one_or_none()
    
    if existing_budget:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Budget already exists for this event"
        )
    
    # Create budget
    budget = Budget(
        event_name=budget_data.event_name,
        total_budget=budget_data.total_budget,
        description=budget_data.description,
        created_by=current_user.id
    )
    
    db.add(budget)
    await db.commit()
    await db.refresh(budget)
    
    return BudgetResponse(
        id=budget.id,
        event_name=budget.event_name,
        total_budget=budget.total_budget,
        allocated_amount=budget.allocated_amount,
        spent_amount=budget.spent_amount,
        remaining_amount=budget.total_budget - budget.allocated_amount,
        description=budget.description,
        created_by=budget.created_by,
        created_at=budget.created_at,
        updated_at=budget.updated_at,
        is_active=budget.is_active,
        creator_name=current_user.full_name
    )


@router.get("/", response_model=List[BudgetResponse])
async def get_budgets(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    event_name: Optional[str] = Query(None),
    active_only: bool = Query(True),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[BudgetResponse]:
    """
    Get budgets (admin/organizer only)
    """
    if current_user.role not in ["admin", "organizer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Build query
    query = select(Budget, User).join(User, Budget.created_by == User.id)
    
    if event_name:
        query = query.where(Budget.event_name.ilike(f"%{event_name}%"))
    if active_only:
        query = query.where(Budget.is_active)
    
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    budgets_with_users = result.all()
    
    return [
        BudgetResponse(
            id=budget.id,
            event_name=budget.event_name,
            total_budget=budget.total_budget,
            allocated_amount=budget.allocated_amount,
            spent_amount=budget.spent_amount,
            remaining_amount=budget.total_budget - budget.allocated_amount,
            description=budget.description,
            created_by=budget.created_by,
            created_at=budget.created_at,
            updated_at=budget.updated_at,
            is_active=budget.is_active,
            creator_name=user.full_name
        )
        for budget, user in budgets_with_users
    ]


@router.get("/{budget_id}", response_model=BudgetResponse)
async def get_budget(
    budget_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> BudgetResponse:
    """
    Get specific budget details
    """
    if current_user.role not in ["admin", "organizer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    result = await db.execute(
        select(Budget, User).join(User, Budget.created_by == User.id)
        .where(Budget.id == budget_id)
    )
    budget_data = result.first()
    
    if not budget_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found"
        )
    
    budget, user = budget_data
    
    return BudgetResponse(
        id=budget.id,
        event_name=budget.event_name,
        total_budget=budget.total_budget,
        allocated_amount=budget.allocated_amount,
        spent_amount=budget.spent_amount,
        remaining_amount=budget.total_budget - budget.allocated_amount,
        description=budget.description,
        created_by=budget.created_by,
        created_at=budget.created_at,
        updated_at=budget.updated_at,
        is_active=budget.is_active,
        creator_name=user.full_name
    )


@router.put("/{budget_id}", response_model=BudgetResponse)
async def update_budget(
    budget_id: int,
    update_data: BudgetUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> BudgetResponse:
    """
    Update budget details (admin/organizer only)
    """
    if current_user.role not in ["admin", "organizer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    result = await db.execute(
        select(Budget).where(Budget.id == budget_id)
    )
    budget = result.scalar_one_or_none()
    
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found"
        )
    
    # Update fields
    update_fields = update_data.dict(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(budget, field, value)
    
    budget.updated_at = datetime.now()
    
    await db.commit()
    await db.refresh(budget)
    
    return BudgetResponse(
        id=budget.id,
        event_name=budget.event_name,
        total_budget=budget.total_budget,
        allocated_amount=budget.allocated_amount,
        spent_amount=budget.spent_amount,
        remaining_amount=budget.total_budget - budget.allocated_amount,
        description=budget.description,
        created_by=budget.created_by,
        created_at=budget.created_at,
        updated_at=budget.updated_at,
        is_active=budget.is_active,
        creator_name=current_user.full_name
    )


@router.post("/{budget_id}/categories", response_model=CategoryResponse)
async def create_budget_category(
    budget_id: int,
    category_data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> CategoryResponse:
    """
    Create budget category (admin/organizer only)
    """
    if current_user.role not in ["admin", "organizer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Verify budget exists
    result = await db.execute(
        select(Budget).where(Budget.id == budget_id)
    )
    budget = result.scalar_one_or_none()
    
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found"
        )
    
    # Check if category name already exists for this budget
    result = await db.execute(
        select(BudgetCategory).where(
            BudgetCategory.budget_id == budget_id,
            BudgetCategory.name == category_data.name
        )
    )
    existing_category = result.scalar_one_or_none()
    
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category name already exists for this budget"
        )
    
    # Create category
    category = BudgetCategory(
        budget_id=budget_id,
        name=category_data.name,
        allocated_amount=category_data.allocated_amount,
        description=category_data.description
    )
    
    db.add(category)
    
    # Update budget allocated amount
    budget.allocated_amount += category_data.allocated_amount
    
    await db.commit()
    await db.refresh(category)
    
    return CategoryResponse(
        id=category.id,
        budget_id=category.budget_id,
        name=category.name,
        allocated_amount=category.allocated_amount,
        spent_amount=category.spent_amount,
        remaining_amount=category.allocated_amount - category.spent_amount,
        description=category.description,
        created_at=category.created_at,
        is_active=category.is_active
    )


@router.get("/{budget_id}/categories", response_model=List[CategoryResponse])
async def get_budget_categories(
    budget_id: int,
    active_only: bool = Query(True),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[CategoryResponse]:
    """
    Get budget categories
    """
    if current_user.role not in ["admin", "organizer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Build query
    query = select(BudgetCategory).where(BudgetCategory.budget_id == budget_id)
    
    if active_only:
        query = query.where(BudgetCategory.is_active)
    
    result = await db.execute(query)
    categories = result.scalars().all()
    
    return [
        CategoryResponse(
            id=category.id,
            budget_id=category.budget_id,
            name=category.name,
            allocated_amount=category.allocated_amount,
            spent_amount=category.spent_amount,
            remaining_amount=category.allocated_amount - category.spent_amount,
            description=category.description,
            created_at=category.created_at,
            is_active=category.is_active
        )
        for category in categories
    ]


@router.post("/expenses", response_model=ExpenseResponse)
async def create_expense(
    expense_data: ExpenseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> ExpenseResponse:
    """
    Create new expense
    """
    # Verify category exists
    result = await db.execute(
        select(BudgetCategory).where(BudgetCategory.id == expense_data.category_id)
    )
    category = result.scalar_one_or_none()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget category not found"
        )
    
    # Create expense
    expense = Expense(
        category_id=expense_data.category_id,
        vendor_name=expense_data.vendor_name,
        description=expense_data.description,
        amount=expense_data.amount,
        receipt_url=expense_data.receipt_url,
        notes=expense_data.notes,
        submitted_by=current_user.id,
        status=ExpenseStatus.PENDING
    )
    
    db.add(expense)
    await db.commit()
    await db.refresh(expense)
    
    return ExpenseResponse(
        id=expense.id,
        category_id=expense.category_id,
        vendor_name=expense.vendor_name,
        description=expense.description,
        amount=expense.amount,
        receipt_url=expense.receipt_url,
        notes=expense.notes,
        status=expense.status,
        submitted_by=expense.submitted_by,
        submitted_at=expense.submitted_at,
        approved_by=expense.approved_by,
        approved_at=expense.approved_at,
        category_name=category.name,
        submitter_name=current_user.full_name,
        approver_name=None
    )


@router.get("/expenses", response_model=List[ExpenseResponse])
async def get_expenses(
    category_id: Optional[int] = Query(None),
    status_filter: Optional[ExpenseStatus] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[ExpenseResponse]:
    """
    Get expenses
    """
    # Build base query with joins
    query = select(
        Expense, 
        BudgetCategory,
        User.full_name.label("submitter_name")
    ).join(
        BudgetCategory, Expense.category_id == BudgetCategory.id
    ).join(
        User, Expense.submitted_by == User.id
    )
    
    # Apply filters
    if category_id:
        query = query.where(Expense.category_id == category_id)
    if status_filter:
        query = query.where(Expense.status == status_filter)
    
    # If not admin/organizer, only show user's own expenses
    if current_user.role not in ["admin", "organizer"]:
        query = query.where(Expense.submitted_by == current_user.id)
    
    query = query.order_by(Expense.submitted_at.desc()).offset(skip).limit(limit)
    
    result = await db.execute(query)
    expense_data = result.all()
    
    # Get approver names for approved expenses
    expense_responses = []
    for expense, category, submitter_name in expense_data:
        approver_name = None
        if expense.approved_by:
            approver_result = await db.execute(
                select(User.full_name).where(User.id == expense.approved_by)
            )
            approver_name = approver_result.scalar_one_or_none()
        
        expense_responses.append(ExpenseResponse(
            id=expense.id,
            category_id=expense.category_id,
            vendor_name=expense.vendor_name,
            description=expense.description,
            amount=expense.amount,
            receipt_url=expense.receipt_url,
            notes=expense.notes,
            status=expense.status,
            submitted_by=expense.submitted_by,
            submitted_at=expense.submitted_at,
            approved_by=expense.approved_by,
            approved_at=expense.approved_at,
            category_name=category.name,
            submitter_name=submitter_name,
            approver_name=approver_name
        ))
    
    return expense_responses


@router.put("/expenses/{expense_id}/approve", response_model=ExpenseResponse)
async def approve_expense(
    expense_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ExpenseResponse:
    """
    Approve expense (admin/organizer only)
    """
    if current_user.role not in ["admin", "organizer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Get expense with category and submitter info
    result = await db.execute(
        select(Expense, BudgetCategory, User.full_name.label("submitter_name"))
        .join(BudgetCategory, Expense.category_id == BudgetCategory.id)
        .join(User, Expense.submitted_by == User.id)
        .where(Expense.id == expense_id)
    )
    expense_data = result.first()
    
    if not expense_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    
    expense, category, submitter_name = expense_data
    
    if expense.status != ExpenseStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Expense is not in pending status"
        )
    
    # Update expense
    expense.status = ExpenseStatus.APPROVED
    expense.approved_by = current_user.id
    expense.approved_at = datetime.now()
    
    # Update category spent amount
    category.spent_amount += expense.amount
    
    await db.commit()
    await db.refresh(expense)
    
    return ExpenseResponse(
        id=expense.id,
        category_id=expense.category_id,
        vendor_name=expense.vendor_name,
        description=expense.description,
        amount=expense.amount,
        receipt_url=expense.receipt_url,
        notes=expense.notes,
        status=expense.status,
        submitted_by=expense.submitted_by,
        submitted_at=expense.submitted_at,
        approved_by=expense.approved_by,
        approved_at=expense.approved_at,
        category_name=category.name,
        submitter_name=submitter_name,
        approver_name=current_user.full_name
    )
