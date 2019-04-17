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

# ...