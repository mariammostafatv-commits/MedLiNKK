"""
MedLink Payment Integration Helper
Use this module to initiate payments from desktop app or provider APIs

Author: Youssef Mekkkawy
Location: payment_gateway/payment_helper.py
"""
import webbrowser
import uuid
import time
import requests
from typing import Optional, Dict
from datetime import datetime


class PaymentGateway:
    """Helper class to integrate MedLink Payment Gateway"""
    
    def __init__(self, gateway_url: str = "http://localhost:8005"):
        self.gateway_url = gateway_url
    
    def initiate_payment(
        self,
        amount: float,
        patient_id: str,
        service: str = "Medical Service",
        auto_open_browser: bool = True
    ) -> str:
        """
        Initiate a payment and open browser
        
        Args:
            amount: Payment amount in EGP
            patient_id: Patient national ID
            service: Description of service
            auto_open_browser: Whether to open browser automatically
        
        Returns:
            invoice_id: Unique invoice ID to track payment
        
        Example:
            gateway = PaymentGateway()
            invoice = gateway.initiate_payment(
                amount=500.00,
                patient_id="29501012345678",
                service="Lab Test - Complete Blood Count"
            )
            print(f"Payment initiated: {invoice}")
        """
        
        # Generate unique invoice ID
        invoice_id = f"INV-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"
        
        # Build checkout URL
        checkout_url = (
            f"{self.gateway_url}/checkout?"
            f"amount={amount}&"
            f"invoice_id={invoice_id}&"
            f"patient_id={patient_id}&"
            f"service={service.replace(' ', '%20')}"
        )
        
        print(f"🏦 Initiating payment...")
        print(f"   Amount: {amount} EGP")
        print(f"   Invoice: {invoice_id}")
        print(f"   Patient: {patient_id}")
        
        if auto_open_browser:
            # Open payment page in default browser
            webbrowser.open(checkout_url)
            print(f"✅ Payment page opened in browser")
        else:
            print(f"🔗 Payment URL: {checkout_url}")
        
        return invoice_id
    
    def check_payment_status(self, invoice_id: str) -> Optional[Dict]:
        """
        Check payment status by invoice ID
        
        Args:
            invoice_id: Invoice ID returned by initiate_payment()
        
        Returns:
            Payment status dictionary or None if not found
        
        Example:
            status = gateway.check_payment_status("INV-20241215-ABC123")
            if status and status['status'] == 'completed':
                print("Payment successful!")
        """
        try:
            response = requests.get(
                f"{self.gateway_url}/api/payment/status/{invoice_id}",
                timeout=5
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print(f"Error checking payment status: {e}")
            return None
    
    def wait_for_payment(
        self,
        invoice_id: str,
        timeout: int = 300,
        check_interval: int = 2
    ) -> bool:
        """
        Wait for payment to complete (polling method)
        
        Args:
            invoice_id: Invoice ID to monitor
            timeout: Maximum time to wait (seconds)
            check_interval: How often to check (seconds)
        
        Returns:
            True if payment completed, False if timeout/failed
        
        Example:
            invoice = gateway.initiate_payment(500, "29501012345678")
            success = gateway.wait_for_payment(invoice, timeout=180)
            if success:
                print("Payment received!")
        """
        start_time = time.time()
        
        print(f"⏳ Waiting for payment completion...")
        print(f"   Invoice: {invoice_id}")
        print(f"   Timeout: {timeout}s")
        
        while (time.time() - start_time) < timeout:
            status = self.check_payment_status(invoice_id)
            
            if status:
                if status['status'] == 'completed':
                    print(f"✅ Payment completed!")
                    print(f"   Transaction ID: {status.get('transaction_id')}")
                    return True
                elif status['status'] == 'failed':
                    print(f"❌ Payment failed")
                    return False
            
            time.sleep(check_interval)
        
        print(f"⏰ Payment timeout after {timeout}s")
        return False


# ==================== USAGE EXAMPLES ====================

def example_basic_payment():
    """Example: Basic payment flow"""
    gateway = PaymentGateway()
    
    # Initiate payment (opens browser)
    invoice_id = gateway.initiate_payment(
        amount=500.00,
        patient_id="29501012345678",
        service="Lab Test - Complete Blood Count"
    )
    
    # Wait for payment (blocks until complete or timeout)
    success = gateway.wait_for_payment(invoice_id, timeout=180)
    
    if success:
        print("✅ Payment successful - proceeding with lab test submission")
        return True
    else:
        print("❌ Payment failed - lab test not submitted")
        return False


def example_async_payment():
    """Example: Non-blocking payment check"""
    gateway = PaymentGateway()
    
    # Initiate payment
    invoice_id = gateway.initiate_payment(
        amount=500.00,
        patient_id="29501012345678",
        service="Hospital Admission Fee"
    )
    
    # Don't block - just save invoice ID
    print(f"Invoice saved: {invoice_id}")
    print("User can pay later, we'll check periodically")
    
    # Later, check status manually
    time.sleep(30)  # Simulate doing other work
    
    status = gateway.check_payment_status(invoice_id)
    if status and status['status'] == 'completed':
        print("Payment completed!")


def example_desktop_app_integration():
    """Example: Integration with desktop app button"""
    import customtkinter as ctk
    
    def on_pay_button_click():
        """Called when user clicks 'Pay Now' in desktop app"""
        gateway = PaymentGateway()
        
        # Get payment details from UI
        amount = 500.00
        patient_id = "29501012345678"
        service = "Lab Test Fee"
        
        # Open payment browser
        invoice_id = gateway.initiate_payment(amount, patient_id, service)
        
        # Store invoice in app state for later checking
        app.current_invoice = invoice_id
        
        # Start background thread to check payment
        # (In real implementation, use threading or async)
        print(f"Payment initiated: {invoice_id}")
    
    # In your CTkButton:
    # pay_button = ctk.CTkButton(
    #     parent,
    #     text="💳 Pay Now",
    #     command=on_pay_button_click
    # )


# ==================== QUICK TEST ====================

if __name__ == "__main__":
    print("="*60)
    print("MedLink Payment Gateway - Integration Test")
    print("="*60)
    
    # Test payment initiation
    gateway = PaymentGateway()
    
    print("\n1️⃣ Initiating test payment...")
    invoice = gateway.initiate_payment(
        amount=500.00,
        patient_id="29501012345678",
        service="Test Payment"
    )
    
    print(f"\n2️⃣ Invoice created: {invoice}")
    print("   Browser should open with payment page")
    print("   Use test card: 4532 1234 5678 9012")
    
    print("\n3️⃣ Checking payment status...")
    status = gateway.check_payment_status(invoice)
    print(f"   Status: {status}")
    
    print("\n" + "="*60)
    print("Test complete!")
    print("="*60)