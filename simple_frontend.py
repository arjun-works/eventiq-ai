"""
Simple EventIQ Frontend without Streamlit
A basic desktop GUI using tkinter (built-in with Python)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import urllib.request
import urllib.error
import json
import threading

class EventIQApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EventIQ - Event Management System")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # API base URL
        self.api_base = "http://localhost:8000"
        self.access_token = None
        self.current_user = None
        
        # Create the main interface
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="EventIQ", font=('Arial', 24, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Login section
        self.login_frame = ttk.LabelFrame(main_frame, text="Login", padding="20")
        self.login_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Email field
        ttk.Label(self.login_frame, text="Email:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.email_var = tk.StringVar(value="admin@eventiq.com")
        email_entry = ttk.Entry(self.login_frame, textvariable=self.email_var, width=30)
        email_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # Password field
        ttk.Label(self.login_frame, text="Password:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.password_var = tk.StringVar(value="password")
        password_entry = ttk.Entry(self.login_frame, textvariable=self.password_var, show="*", width=30)
        password_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Login button
        login_btn = ttk.Button(self.login_frame, text="Login", command=self.login)
        login_btn.grid(row=2, column=0, columnspan=2, pady=(20, 0))
        
        # Test credentials info
        info_text = "Test Credentials:\nAdmin: admin@eventiq.com / password\nUser: user@example.com / password"
        info_label = ttk.Label(self.login_frame, text=info_text, font=('Arial', 9), foreground='gray')
        info_label.grid(row=3, column=0, columnspan=2, pady=(10, 0))
        
        # Dashboard section (initially hidden)
        self.dashboard_frame = ttk.LabelFrame(main_frame, text="Dashboard", padding="20")
        
        # User info
        self.user_info_frame = ttk.Frame(self.dashboard_frame)
        self.user_info_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(20, 0))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
    def login(self):
        """Handle login"""
        email = self.email_var.get()
        password = self.password_var.get()
        
        if not email or not password:
            messagebox.showerror("Error", "Please enter both email and password")
            return
        
        self.status_var.set("Logging in...")
        
        # Use threading to prevent UI freezing
        def login_thread():
            try:
                data = json.dumps({"username": email, "password": password})
                req = urllib.request.Request(
                    f"{self.api_base}/api/v1/auth/login",
                    data=data.encode('utf-8'),
                    headers={'Content-Type': 'application/json'}
                )
                
                with urllib.request.urlopen(req, timeout=10) as response:
                    if response.code == 200:
                        response_data = json.loads(response.read().decode('utf-8'))
                        self.access_token = response_data["access_token"]
                        self.current_user = response_data["user"]
                        
                        # Update UI in main thread
                        self.root.after(0, self.show_dashboard)
                        self.root.after(0, lambda: self.status_var.set("Login successful"))
                    else:
                        error_msg = "Login failed"
                        self.root.after(0, lambda: messagebox.showerror("Login Failed", error_msg))
                        self.root.after(0, lambda: self.status_var.set("Login failed"))
                        
            except urllib.error.URLError:
                self.root.after(0, lambda: messagebox.showerror("Connection Error", 
                    "Cannot connect to server. Make sure the test server is running on localhost:8000"))
                self.root.after(0, lambda: self.status_var.set("Connection failed"))
            except Exception as e:
                error_msg = f"An error occurred: {str(e)}"
                self.root.after(0, lambda msg=error_msg: messagebox.showerror("Error", msg))
                self.root.after(0, lambda: self.status_var.set("Error occurred"))
        
        threading.Thread(target=login_thread, daemon=True).start()
    
    def show_dashboard(self):
        """Show the dashboard after successful login"""
        # Hide login frame
        self.login_frame.grid_remove()
        
        # Show dashboard frame
        self.dashboard_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        
        # Clear previous user info
        for widget in self.user_info_frame.winfo_children():
            widget.destroy()
        
        # Display user information
        user = self.current_user
        ttk.Label(self.user_info_frame, text=f"Welcome, {user['full_name']}!", 
                 font=('Arial', 16, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # User details
        details = [
            ("Email", user['email']),
            ("Role", user['role'].title()),
            ("Status", "Active" if user['is_active'] else "Inactive"),
            ("Verified", "Yes" if user['is_verified'] else "No"),
            ("User ID", str(user['id']))
        ]
        
        for i, (label, value) in enumerate(details):
            ttk.Label(self.user_info_frame, text=f"{label}:").grid(row=i+1, column=0, sticky=tk.W, padx=(0, 10))
            ttk.Label(self.user_info_frame, text=value, font=('Arial', 9, 'bold')).grid(row=i+1, column=1, sticky=tk.W)
        
        # Action buttons
        actions_frame = ttk.Frame(self.dashboard_frame)
        actions_frame.grid(row=1, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(actions_frame, text="Test API Health", command=self.test_health).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(actions_frame, text="Logout", command=self.logout).grid(row=0, column=1, padx=(10, 0))
        
        # Server status
        status_frame = ttk.LabelFrame(self.dashboard_frame, text="Server Status", padding="10")
        status_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(20, 0))
        
        self.server_status_var = tk.StringVar(value="Checking...")
        ttk.Label(status_frame, textvariable=self.server_status_var).grid(row=0, column=0)
        
        # Check server health
        self.test_health()
    
    def test_health(self):
        """Test server health"""
        def health_thread():
            try:
                req = urllib.request.Request(f"{self.api_base}/health")
                with urllib.request.urlopen(req, timeout=5) as response:
                    if response.code == 200:
                        self.root.after(0, lambda: self.server_status_var.set("✅ Server is healthy"))
                    else:
                        self.root.after(0, lambda: self.server_status_var.set("❌ Server returned error"))
            except Exception as e:
                error_msg = f"❌ Health check failed: {str(e)}"
                self.root.after(0, lambda msg=error_msg: self.server_status_var.set(msg))
        
        threading.Thread(target=health_thread, daemon=True).start()
    
    def logout(self):
        """Handle logout"""
        self.access_token = None
        self.current_user = None
        
        # Hide dashboard
        self.dashboard_frame.grid_remove()
        
        # Show login frame
        self.login_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.status_var.set("Logged out")

def main():
    """Main function to run the application"""
    root = tk.Tk()
    EventIQApp(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
