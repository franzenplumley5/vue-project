
import os
import zipfile
import requests
import shutil
import platform
from pathlib import Path

def get_chrome_version_mac():
    try:
        from subprocess import check_output
        output = check_output(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'])
        return output.decode().strip().split()[-1]
    except:
        return None

def download_driver(version, output_path):
    major = version.split('.')[0]
    url = f"https://storage.googleapis.com/chrome-for-testing-public/{version}/mac-arm64/chromedriver-mac-arm64.zip"
    local_zip = "chromedriver_tmp.zip"
    
    print(f"🔍 下载 ChromeDriver v{version}（主版本：{major}）")
    try:
        with requests.get(url, stream=True) as r:
            with open(local_zip, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        with zipfile.ZipFile(local_zip, 'r') as zip_ref:
            zip_ref.extractall("chromedriver_tmp")
        driver_bin = Path("chromedriver_tmp/chromedriver-mac-arm64/chromedriver")
        driver_bin.chmod(0o755)
        shutil.move(str(driver_bin), output_path)
        shutil.rmtree("chromedriver_tmp")
        os.remove(local_zip)
        print(f"✅ ChromeDriver 已保存至: {output_path}")
        return True
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        return False

def main():
    print("🚀 自动获取本机 Chrome 版本...")
    chrome_version = get_chrome_version_mac()
    if not chrome_version:
        print("❌ 无法获取 Chrome 版本")
        return
    print(f"✅ 当前 Chrome 版本: {chrome_version}")

    output_path = Path("drivers/chromedriver")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    success = download_driver(chrome_version, str(output_path))

    if success:
        print("✅ 你现在可以在 Selenium 中使用该路径:\n    executable_path='drivers/chromedriver'")
    else:
        print("⚠️ 请手动下载并放入 drivers/ 目录中")

if __name__ == "__main__":
    main()
