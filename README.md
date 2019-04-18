# asyncio-src
asyncio源码解析

1. 现阶段目标先通读一遍源码，写好注释。
2. 之后会画出流程图，补充读懂源码的额外知识，尽情期待😍😍！


### 阅读顺序
1. 从`asyncio.run()`开始，传入一个协程对象`main`，返回一个`loop.run_until_complete(main)`。
里面大概执行了如下几个关键的函数
    1. `events.new_event_loop()` 创建一个事件循环
    2. `events.set_event_loop(loop)` 设置loop为当前的事件循环
    3. `loop.run_until_complete(main)` 运行事件循环，直到Future完成
    
2. `loop.run_until_complete()`里面执行的是`run_forever()`。
    1. `run_forever()`中设置了_running_loop,然后一直调用`_run_once()`这个方法，
    可以说这个方法是任务的核心调度,配合select/epoll等系统调用完成事件循环。
    2. `_run_once()`这个方法的逻辑是先把整理`_scheduled`的要执行的和`selcet`中就绪的事件
    添加到`_ready`队列中去，然后遍历`_ready`队列（ `collections.deque()`）,对列中的任务其实一个`handle`
    对象，执行`handle._run()`会去调用 `Task._step()`方法, `_step()`实际调用的是`coro.send(None)`。
    3. `coro.send(None)`是协程中的概念，它会接着上次`yeild`的地方继续执行下去。
    
    
    
    

# ...