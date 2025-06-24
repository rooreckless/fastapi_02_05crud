#-----------------
# 1. 同期処理
import time
def sync_task(name):
    print(f"{name} タスク開始")
    time.sleep(2)
    print(f"{name} タスク終了")

# 同期処理を何回か読んでみる
def run_sync_tasks():
    sync_task("タスク1")
    sync_task("タスク2")
    sync_task("タスク3")
print("---同期処理を実行する例---")
run_sync_tasks()

print("----------------------------")

import asyncio
async def async_task(name):
    print(f"{name} タスク開始")
    await asyncio.sleep(2)
    print(f"{name} タスク終了")

async def run_async_tasks():
    await asyncio.gather(
        async_task("タスクA"),
        async_task("タスクB"),
        async_task("タスクC")
    )
print("---非同期処理を実行する例---")
asyncio.run(run_async_tasks())


#--実行した時のターミナルの様子が以下----

# roo_wsl@roo-TUF-A16-24:~/fastapi_02_05crud$ python3 sync_async_test.py 

# ---同期処理を実行する例---
# タスク1 タスク開始
# タスク1 タスク終了
# タスク2 タスク開始
# タスク2 タスク終了
# タスク3 タスク開始
# タスク3 タスク終了
# ----------------------------
# ---非同期処理を実行する例---
# タスクA タスク開始
# タスクB タスク開始
# タスクC タスク開始
# タスクA タスク終了
# タスクB タスク終了
# タスクC タスク終了

#つまり、asyncioをつかうと非同期処理を実行できる