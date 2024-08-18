import asyncio
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from io import BytesIO
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
import base64

app = FastAPI()

def safe_int(value: str, default: int) -> int:
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

async def take_screenshot(url: str, format: str = 'png', width: int = 1920, height: int = 1080, 
                          full_page: bool = False, mobile: bool = False, delay: int = 0, 
                          custom_js: str = None, user_agent: str = None):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                viewport={'width': width, 'height': height},
                is_mobile=mobile,
                user_agent=user_agent
            )
            page = await context.new_page()
            await page.goto(url)

            if delay > 0:
                await asyncio.sleep(delay)

            if custom_js:
                await page.evaluate(custom_js)

            screenshot_options = {'full_page': full_page}
            screenshot_data = await page.screenshot(**screenshot_options)
            await browser.close()

            if format == 'base64':
                return base64.b64encode(screenshot_data).decode('utf-8')
            else:
                return screenshot_data

    except PlaywrightTimeoutError as e:
        raise HTTPException(status_code=504, detail=f"Timeout while navigating to {url}.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Welcome to the Screenshot API! Documentation at: http://127.0.0.1:8000/docs"}

@app.get("/screenshot")
async def screenshot(
    url: str,
    format: str = Query('png', pattern="^(png|base64)$", description="Format of the screenshot."),
    width: int = Query(1920, description="Width of the browser viewport."),
    height: int = Query(1080, description="Height of the browser viewport."),
    full_page: bool = Query(False, description="Capture the full page."),
    mobile: bool = Query(False, description="Simulate a mobile device."),
    delay: int = Query(0, description="Delay in seconds before taking the screenshot."),
    custom_js: str = Query(None, description="Custom JavaScript to execute before taking the screenshot."),
    user_agent: str = Query(None, description="Custom User-Agent string.")
):
    screenshot_result = await take_screenshot(url, format, width, height, full_page, mobile, delay, custom_js, user_agent)

    if format == 'base64':
        return JSONResponse(content={"screenshot": screenshot_result})
    else:
        img_io = BytesIO(screenshot_result)
        img_io.seek(0)
        return StreamingResponse(img_io, media_type="image/png")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
