#!/usr/bin/env python3
"""
AI Memory API Client Example

This script demonstrates how to use the AI Memory API.
"""

import requests
import json
from typing import Optional


class AIMemoryClient:
    """Client for AI Memory API"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.api_base = f"{base_url}/api/v1"
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
    
    def _headers(self) -> dict:
        """Get request headers with auth token"""
        headers = {"Content-Type": "application/json"}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        return headers
    
    def register(self, email: str, password: str) -> dict:
        """Register a new user"""
        url = f"{self.api_base}/auth/register"
        data = {"email": email, "password": password}
        
        response = requests.post(url, json=data)
        response.raise_for_status()
        
        result = response.json()
        self.access_token = result.get("access_token")
        self.refresh_token = result.get("refresh_token")
        
        return result
    
    def login(self, email: str, password: str) -> dict:
        """Login with email and password"""
        url = f"{self.api_base}/auth/login"
        data = {"email": email, "password": password}
        
        response = requests.post(url, json=data)
        response.raise_for_status()
        
        result = response.json()
        self.access_token = result.get("access_token")
        self.refresh_token = result.get("refresh_token")
        
        return result
    
    def get_profile(self) -> dict:
        """Get current user profile"""
        url = f"{self.api_base}/auth/me"
        
        response = requests.get(url, headers=self._headers())
        response.raise_for_status()
        
        return response.json()
    
    def upload_files(self, files: list) -> dict:
        """Upload files for processing"""
        url = f"{self.api_base}/upload/"
        
        files_data = [("files", open(f, "rb")) for f in files]
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        response = requests.post(url, files=files_data, headers=headers)
        response.raise_for_status()
        
        # Close file handles
        for _, file_obj in files_data:
            file_obj.close()
        
        return response.json()
    
    def send_message(self, message: str, context_id: Optional[str] = None) -> dict:
        """Send a chat message"""
        url = f"{self.api_base}/chat/"
        data = {"message": message}
        if context_id:
            data["context_id"] = context_id
        
        response = requests.post(url, json=data, headers=self._headers())
        response.raise_for_status()
        
        return response.json()
    
    def get_stats(self) -> dict:
        """Get admin statistics (admin only)"""
        url = f"{self.api_base}/admin/stats"
        
        response = requests.get(url, headers=self._headers())
        response.raise_for_status()
        
        return response.json()


def main():
    """Example usage"""
    client = AIMemoryClient()
    
    # Example 1: Register a new user
    print("=== Registering new user ===")
    try:
        result = client.register("user@example.com", "password123")
        print(f"✓ Registered: {result['user']['email']}")
        print(f"✓ Role: {result['user']['role']}")
    except requests.exceptions.HTTPError as e:
        print(f"✗ Registration failed: {e}")
    
    # Example 2: Get user profile
    print("\n=== Getting user profile ===")
    try:
        profile = client.get_profile()
        print(f"✓ Email: {profile['email']}")
        print(f"✓ Role: {profile['role']}")
        print(f"✓ Active: {profile['is_active']}")
    except requests.exceptions.HTTPError as e:
        print(f"✗ Failed to get profile: {e}")
    
    # Example 3: Send a chat message
    print("\n=== Sending chat message ===")
    try:
        response = client.send_message("Hello, AI Memory!")
        print(f"✓ Reply: {response['reply']}")
    except requests.exceptions.HTTPError as e:
        print(f"✗ Chat failed: {e}")
    
    # Example 4: Upload files (if you have test files)
    # print("\n=== Uploading files ===")
    # try:
    #     result = client.upload_files(["test.pdf", "test.docx"])
    #     print(f"✓ Upload ID: {result['upload_id']}")
    #     print(f"✓ Pages: {result['page_count']}")
    #     print(f"✓ Price: ${result['price']}")
    # except requests.exceptions.HTTPError as e:
    #     print(f"✗ Upload failed: {e}")


if __name__ == "__main__":
    main()
