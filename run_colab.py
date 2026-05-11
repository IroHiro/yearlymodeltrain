# run_colab.py
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Your Colab notebook ID (get from URL)
NOTEBOOK_ID = "YOUR_NOTEBOOK_ID_HERE"  # Replace with your actual ID

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
        # Initialize the driver
        driver = webdriver.Chrome(options=chrome_options)
        print("✅ Chrome driver initialized")
        
        # Construct Colab URL with force flag
        colab_url = f"https://colab.research.google.com/drive/{NOTEBOOK_ID}#force=true"
        print(f"📂 Opening Colab notebook: {colab_url}")
        driver.get(colab_url)
        
        # Wait for page to load
        time.sleep(15)
        print("⏳ Page loaded, waiting for interface...")
        
        # Try to click Runtime menu (multiple selector attempts for robustness)
        runtime_selectors = [
            "//*[contains(text(), 'Runtime')]",
            "//span[contains(text(), 'Runtime')]",
            "//*[@id='runtime-menu']",
            "//button[@aria-label='Runtime']"
        ]
        
        runtime_button = None
        for selector in runtime_selectors:
            try:
                runtime_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                if runtime_button:
                    break
            except:
                continue
        
        if runtime_button:
            runtime_button.click()
            print("✅ Clicked Runtime menu")
            time.sleep(2)
        else:
            print("⚠️ Could not find Runtime menu")
        
        # Try to click Run all
        run_all_selectors = [
            "//*[contains(text(), 'Run all')]",
            "//span[contains(text(), 'Run all')]",
            "//*[@aria-label='Run all cells']",
            "//button[contains(@aria-label, 'Run all')]"
        ]
        
        run_all_button = None
        for selector in run_all_selectors:
            try:
                run_all_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                if run_all_button:
                    break
            except:
                continue
        
        if run_all_button:
            run_all_button.click()
            print("✅ Clicked Run all! Notebook execution started.")
        else:
            print("⚠️ Could not find Run all button")
            
        # Let the notebook run for a while
        print("⏳ Allowing 20 minutes for notebook execution...")
        time.sleep(1200)  # 20 minutes - adjust as needed
        
        print("🎉 Colab automation completed (or timed out)")
        
    except Exception as e:
        print(f"❌ Error during automation: {e}")
        
    finally:
        if driver:
            driver.quit()
            print("🔒 Browser closed")

if __name__ == "__main__":
    run_colab_notebook()
