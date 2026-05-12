# run_colab.py
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Your Colab notebook ID - ONLY the ID part
NOTEBOOK_ID = "1JXUXrkbsbkJPniHNVdekycrYl-ad8y5m#scrollTo=85uUQhGyzRuJ"

def run_colab_notebook():
    """Attempt to open and run a Colab notebook automatically"""
    
    print("🚀 Starting Colab automation...")
    
    # Configure Chrome for headless operation
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run without GUI
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
    driver = None
    try:
        # Initialize the driver with webdriver-manager
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("✅ Chrome driver initialized")
        
        # Construct Colab URL with force flag
        colab_url = f"https://colab.research.google.com/drive/{NOTEBOOK_ID}#force=true"
        print(f"📂 Opening Colab notebook: {colab_url}")
        driver.get(colab_url)
        
        # Wait for page to load
        time.sleep(15)
        print("⏳ Page loaded, waiting for interface...")
        
        # ============================================
        # STEP 1: Click "Connect" button first (if needed)
        # ============================================
        try:
            # Look for Connect button - common selectors
            connect_selectors = [
                "//*[contains(text(), 'Connect')]",
                "//button[contains(@aria-label, 'Connect')]",
                "//span[text()='Connect']"
            ]
            
            for selector in connect_selectors:
                try:
                    connect_btn = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    if connect_btn:
                        connect_btn.click()
                        print("✅ Connected to runtime")
                        time.sleep(5)
                        break
                except:
                    continue
        except:
            print("⚠️ No Connect button found or already connected")
        
        # ============================================
        # STEP 2: Click Runtime menu using your XPath
        # ============================================
        print("🔍 Looking for Runtime menu...")
        
        # Primary XPath you provided
        runtime_selectors = [
            "//div[normalize-space()='Runtime']",  # Your provided XPath
            "//*[contains(text(), 'Runtime')]",
            "//span[contains(text(), 'Runtime')]",
            "/html/body[1]/div[7]/div[1]/div/div[3]/div[2]/div[2]/div[2]/div/div/div[5]/div/div/div[1]"  # Absolute path
        ]
        
        runtime_button = None
        for selector in runtime_selectors:
            try:
                runtime_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                if runtime_button:
                    print(f"✅ Found Runtime menu with selector: {selector[:50]}...")
                    break
            except:
                continue
        
        if runtime_button:
            runtime_button.click()
            print("✅ Clicked Runtime menu")
            time.sleep(2)
        else:
            print("❌ Could not find Runtime menu")
            # Take screenshot for debugging
            driver.save_screenshot("debug_runtime_not_found.png")
            print("📸 Screenshot saved: debug_runtime_not_found.png")
        
        # ============================================
        # STEP 3: Click "Run all" button using your XPath
        # ============================================
        print("🔍 Looking for Run all button...")
        
        # Primary XPath you provided: /button/span[1]
        run_all_selectors = [
            "/button/span[1]",  # Your provided XPath
            "//span[text()='Run all']",
            "//*[contains(text(), 'Run all')]",
            "//button[contains(@aria-label, 'Run all')]",
            "//button//span[text()='Run all']"
        ]
        
        run_all_button = None
        for selector in run_all_selectors:
            try:
                # Try to find by the parent button first (your XPath)
                if selector == "/button/span[1]":
                    # This XPath finds the span, need to click its parent button
                    span_element = driver.find_element(By.XPATH, selector)
                    run_all_button = span_element.find_element(By.XPATH, "..")
                else:
                    run_all_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                
                if run_all_button:
                    print(f"✅ Found Run all button")
                    break
            except Exception as e:
                continue
        
        if run_all_button:
            run_all_button.click()
            print("✅ Clicked Run all! Notebook execution started.")
        else:
            print("❌ Could not find Run all button")
            driver.save_screenshot("debug_runall_not_found.png")
            print("📸 Screenshot saved: debug_runall_not_found.png")
        
        # ============================================
        # STEP 4: Monitor execution (optional)
        # ============================================
        print("⏳ Allowing 20 minutes for notebook execution...")
        
        # Optional: Look for execution status indicators
        for i in range(20):  # Check every minute for 20 minutes
            time.sleep(60)
            try:
                # Look for "Runtime" menu again - if it's disabled, still running
                runtime_check = driver.find_elements(By.XPATH, "//div[normalize-space()='Runtime']")
                print(f"   Minute {i+1}: Still running...")
            except:
                print(f"   Minute {i+1}: Check failed, but continuing...")
        
        print("🎉 Colab automation completed (or timed out)")
        
    except Exception as e:
        print(f"❌ Error during automation: {e}")
        if driver:
            driver.save_screenshot("debug_error.png")
            print("📸 Error screenshot saved: debug_error.png")
        
    finally:
        if driver:
            driver.quit()
            print("🔒 Browser closed")

if __name__ == "__main__":
    run_colab_notebook()
