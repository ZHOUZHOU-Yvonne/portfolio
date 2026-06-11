"""
猪八戒自动登录 - 需要用户提供短信验证码
Usage: python3 zbj_login.py [--code SMS_CODE]
"""
import sys
import json
import os
from playwright.sync_api import sync_playwright

SESSION_FILE = os.path.expanduser('~/.zbj_session.json')
PHONE = '13051770627'
PASSWORD = 'UDq5VTaFAf8kZeq'

def save_session(context):
    """Save browser session to file for later reuse."""
    cookies = context.cookies()
    with open(SESSION_FILE, 'w') as f:
        json.dump(cookies, f)
    print(f"\n✅ 会话已保存到 {SESSION_FILE}")
    print("   下次运行 zbj_bid.py 将直接使用此会话\n")

def load_session(context):
    """Load saved session if exists."""
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE) as f:
            cookies = json.load(f)
        context.add_cookies(cookies)
        return True
    return False

def login_with_sms(context, page, code):
    """Login using SMS verification code."""
    page.fill('input[type="text"], input[placeholder*="验证码"]', code)
    page.click('button:has-text("登录"), button:has-text("确定"), button:has-text("登 录")')
    page.wait_for_timeout(3000)

    if 'login' not in page.url.lower() and 'passport' not in page.url.lower():
        print("✅ SMS 登录成功！")
        save_session(context)
        return True
    else:
        error = page.text_content('.error, .err, .msg, [class*="error"]') or ''
        print(f"❌ 登录失败: {error}")
        return False

def login_with_password(context, page):
    """Try password login first."""
    # Try to find and fill password login form
    try:
        # Switch to password login tab if needed
        page.click('text=密码登录, text=账号登录, text=账户密码', timeout=3000)
        page.wait_for_timeout(500)
    except:
        pass

    # Fill phone and password
    phone_inputs = page.locator('input[placeholder*="手机"], input[placeholder*="账号"], input[type="text"]').all()
    for inp in phone_inputs:
        try:
            inp.fill(PHONE)
            break
        except:
            continue

    password_inputs = page.locator('input[type="password"]').all()
    for inp in password_inputs:
        try:
            inp.fill(PASSWORD)
            break
        except:
            continue

    # Click login
    page.click('button:has-text("登录"), button:has-text("登 录"), button[type="submit"]')
    page.wait_for_timeout(3000)

    if 'login' not in page.url.lower() and 'passport' not in page.url.lower():
        print("✅ 密码登录成功！")
        save_session(context)
        return True
    else:
        print("   密码登录不可用，尝试短信登录...")
        return False

def main():
    code = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == '--code' else None

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1440, 'height': 900}
        )
        page = context.new_page()

        # Try loading saved session
        if load_session(context) and not code:
            print("📂 使用已保存的会话...")
            page.goto('https://www.zbj.com/')
            page.wait_for_timeout(2000)

            # Check if session is still valid
            if 'login' not in page.url.lower():
                print("✅ 会话有效，已登录！")
                print(f"   当前页面: {page.url}")
                browser.close()
                return
            else:
                print("   会话已过期，重新登录...")

        # Navigate to login page
        print(f"🌐 打开猪八戒登录页...")
        page.goto('https://account.zbj.com/login')
        page.wait_for_timeout(2000)

        # Try password login
        if login_with_password(context, page):
            browser.close()
            return

        # If password login failed, try SMS
        print("📱 发送短信验证码...")

        # Click SMS login tab
        try:
            page.click('text=短信登录, text=验证码登录, text=手机验证码, text=短信验证码登录', timeout=3000)
            page.wait_for_timeout(500)
        except:
            pass

        # Enter phone number
        phone_filled = False
        for inp in page.locator('input[type="text"], input[placeholder*="手机"], input[placeholder*="账号"]').all():
            try:
                inp.fill(PHONE)
                phone_filled = True
                break
            except:
                continue

        if not phone_filled:
            print("❌ 找不到手机号输入框")
            page.screenshot(path='/tmp/zbj_login_error.png')
            print("   截图: /tmp/zbj_login_error.png")
            browser.close()
            return

        # Click send SMS button
        send_clicked = False
        for btn in page.locator('button:has-text("发送"), button:has-text("获取验证码"), span:has-text("发送"), span:has-text("获取")').all():
            try:
                btn.click()
                send_clicked = True
                break
            except:
                continue

        if not send_clicked:
            print("❌ 找不到发送验证码按钮")
            page.screenshot(path='/tmp/zbj_login_error.png')
            browser.close()
            return

        print("✅ 验证码已发送到手机 13051770627")

        if code:
            # Code provided via command line
            if login_with_sms(context, page, code):
                browser.close()
                return
        else:
            # Save context for user to provide code later
            print("\n📱 请用户提供验证码，然后运行:")
            print("   python3 zbj_login.py --code <验证码>")
            # Save page state
            page.screenshot(path='/tmp/zbj_waiting_code.png')
            print("   截图: /tmp/zbj_waiting_code.png")

        browser.close()

if __name__ == '__main__':
    main()
