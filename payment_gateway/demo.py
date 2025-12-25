"""
MedLink Payment Gateway - Demo Script
Quick test of payment gateway functionality

Run this script to test the payment gateway!

Author: Youssef Mekkkawy
"""
import time
from payment_helper import PaymentGateway


def demo_successful_payment():
    """Demo 1: Successful payment flow"""
    print("\n" + "="*70)
    print("DEMO 1: Successful Payment Flow")
    print("="*70)
    
    gateway = PaymentGateway()
    
    print("\n📋 Scenario: Patient needs to pay for lab test")
    print("   Patient ID: 29501012345678")
    print("   Amount: 500.00 EGP")
    print("   Service: Complete Blood Count Test")
    
    print("\n🏦 Initiating payment...")
    invoice = gateway.initiate_payment(
        amount=500.00,
        patient_id="29501012345678",
        service="Lab Test - Complete Blood Count"
    )
    
    print(f"\n✅ Payment page opened in browser")
    print(f"   Invoice ID: {invoice}")
    print(f"\n📝 Instructions:")
    print(f"   1. Browser window should open automatically")
    print(f"   2. Use test card: 4532 1234 5678 9012")
    print(f"   3. CVV: 123, Expiry: 12/25")
    print(f"   4. Click 'Pay Now'")
    
    input("\n⏸️  Press Enter after completing payment in browser...")
    
    print("\n🔍 Checking payment status...")
    status = gateway.check_payment_status(invoice)
    
    if status:
        print(f"\n📊 Payment Status:")
        print(f"   Status: {status.get('status')}")
        if status.get('status') == 'completed':
            print(f"   ✅ Transaction ID: {status.get('transaction_id')}")
            print(f"   💳 Card: {status.get('card_brand')} ****{status.get('card_last4')}")
            print(f"\n🎉 SUCCESS! Payment completed")
        else:
            print(f"   ⏳ Payment still pending")
    else:
        print(f"   ❌ Payment not found or failed")


def demo_declined_payment():
    """Demo 2: Declined payment (using decline test card)"""
    print("\n" + "="*70)
    print("DEMO 2: Declined Payment (Testing Error Handling)")
    print("="*70)
    
    gateway = PaymentGateway()
    
    print("\n📋 Scenario: Testing declined payment")
    print("   Test Card: 4532 8888 8888 8888 (Decline card)")
    
    print("\n🏦 Initiating payment...")
    invoice = gateway.initiate_payment(
        amount=750.00,
        patient_id="29501012345678",
        service="X-Ray Imaging"
    )
    
    print(f"\n✅ Payment page opened")
    print(f"\n📝 Instructions:")
    print(f"   Use DECLINE test card: 4532 8888 8888 8888")
    print(f"   This will simulate a declined payment")
    
    input("\n⏸️  Press Enter after trying the payment...")
    
    status = gateway.check_payment_status(invoice)
    print(f"\n📊 Result: Payment should be declined")


def demo_async_payment():
    """Demo 3: Non-blocking payment check"""
    print("\n" + "="*70)
    print("DEMO 3: Non-Blocking Payment (Continue Working)")
    print("="*70)
    
    gateway = PaymentGateway()
    
    print("\n📋 Scenario: Initiate payment but don't wait")
    print("   Patient can pay later while we do other work")
    
    invoice = gateway.initiate_payment(
        amount=300.00,
        patient_id="29501012345678",
        service="Medication Purchase"
    )
    
    print(f"\n✅ Payment initiated: {invoice}")
    print(f"\n💡 Continuing with other work...")
    print(f"   (Simulating other tasks)")
    
    # Simulate doing other work
    for i in range(5):
        print(f"   Working... {i+1}/5")
        time.sleep(1)
    
    print(f"\n🔍 Now checking if payment was completed...")
    status = gateway.check_payment_status(invoice)
    
    if status and status.get('status') == 'completed':
        print(f"   ✅ Great! Payment completed while we worked")
    else:
        print(f"   ⏳ Payment not completed yet (that's OK)")


def demo_payment_timeout():
    """Demo 4: Wait for payment with timeout"""
    print("\n" + "="*70)
    print("DEMO 4: Waiting for Payment (with timeout)")
    print("="*70)
    
    gateway = PaymentGateway()
    
    print("\n📋 Scenario: Wait for payment, timeout after 60s")
    
    invoice = gateway.initiate_payment(
        amount=1000.00,
        patient_id="29501012345678",
        service="Hospital Consultation Fee"
    )
    
    print(f"\n⏳ Waiting for payment...")
    print(f"   Timeout: 60 seconds")
    print(f"   Complete payment in browser within 60s")
    
    success = gateway.wait_for_payment(invoice, timeout=60)
    
    if success:
        print(f"\n✅ Payment received within timeout!")
    else:
        print(f"\n⏰ Timeout - payment not completed")


def show_test_cards():
    """Show available test cards"""
    print("\n" + "="*70)
    print("💳 AVAILABLE TEST CARDS")
    print("="*70)
    
    print("\n✅ SUCCESS CARDS (Payment will be approved):")
    print("   4532 1234 5678 9012  - Visa (National Bank)")
    print("   4532 1111 1111 1111  - Visa (Banque Misr)")
    print("   5425 2334 3010 9903  - Mastercard (HSBC)")
    print("   5425 1111 1111 1111  - Mastercard (Alexandria Bank)")
    print("   9999 7777 6666 5555  - Fawry")
    
    print("\n❌ DECLINE CARDS (Payment will be declined):")
    print("   4532 8888 8888 8888  - Card Declined")
    print("   5425 8888 8888 8888  - Card Declined")
    
    print("\n⚠️  ERROR CARDS (Simulate errors):")
    print("   4532 0000 0000 0000  - Insufficient Funds")
    
    print("\n📝 For all cards use:")
    print("   CVV: Any 3 digits (e.g., 123)")
    print("   Expiry: Any future date (e.g., 12/25)")
    print("   Name: Any name")
    
    print("\n🌐 Full list: http://localhost:8005/test-cards")


def main_menu():
    """Show demo menu"""
    while True:
        print("\n" + "="*70)
        print("🏦 MEDLINK PAYMENT GATEWAY - DEMO MENU")
        print("="*70)
        print("\n1. Demo: Successful Payment Flow")
        print("2. Demo: Declined Payment (Error Handling)")
        print("3. Demo: Non-Blocking Payment")
        print("4. Demo: Wait for Payment (Timeout)")
        print("5. Show Test Card Numbers")
        print("6. Open Test Cards Page in Browser")
        print("7. Exit")
        
        choice = input("\nEnter choice (1-7): ").strip()
        
        if choice == '1':
            demo_successful_payment()
        elif choice == '2':
            demo_declined_payment()
        elif choice == '3':
            demo_async_payment()
        elif choice == '4':
            demo_payment_timeout()
        elif choice == '5':
            show_test_cards()
        elif choice == '6':
            import webbrowser
            webbrowser.open("http://localhost:8005/test-cards")
            print("\n✅ Opened test cards page in browser")
        elif choice == '7':
            print("\n👋 Goodbye!")
            break
        else:
            print("\n❌ Invalid choice, please try again")


if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║        🏥 MedLink Payment Gateway Demo                  ║
    ║                                                          ║
    ║        Professional Test Payment System                 ║
    ║        Author: Youssef Mekkkawy                         ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    print("\n⚠️  IMPORTANT: Make sure payment gateway is running!")
    print("   Run in another terminal: python main.py")
    print("   Gateway should be at: http://localhost:8005")
    
    input("\n✅ Press Enter when gateway is ready...")
    
    main_menu()