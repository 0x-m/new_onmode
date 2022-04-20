import asyncio
import httpx
from django.http import HttpRequest, HttpResponse, JsonResponse
import time

def api(request: HttpRequest):
    time.sleep(5);
    payload = {"message": "hello world!"}
    if "task_id" in request.GET:
        payload["task_id"] = request.GET["task_id"]
    
    return JsonResponse(payload)


async def http_call_async():
    for num in range(1, 6):
        await asyncio.sleep(1)
        print(num)
    async with httpx.AsyncClient() as client:
        r = await client.get("https://httpbin.org")
        print(r)
    
async def async_view(request):
    loop = asyncio.get_event_loop()
    loop.create_task(http_call_async())
    return HttpResponse('Non-Blocking http request')

    