# 常见设计模式：工厂、发布订阅、装饰器、桥接

这份教辅资料总结四种常见工程设计模式：工厂模式、发布订阅模式、装饰器模式、桥接模式。它们不是 Agent 独有概念，但在 Agent 工程里经常出现：

- 工厂模式：根据配置创建模型、工具、Retriever、Skill。
- 发布订阅模式：把工具调用、评测事件、日志和监控解耦。
- 装饰器模式：给工具或 API 增加日志、权限、缓存、重试、限流。
- 桥接模式：把“抽象能力”和“具体实现”拆开，例如同一个 Agent 支持不同模型、不同检索后端。

## 一、工厂模式

### 1. 核心思想

工厂模式把对象创建逻辑封装起来。调用者不用关心具体怎么 `new`，只通过统一入口拿到需要的对象。

一句话：

> 工厂模式解决“创建逻辑和使用逻辑耦合”的问题。

### 2. 适用场景

- 创建逻辑复杂，需要根据条件决定实例化哪个类。
- 希望调用方和具体类解耦。
- 新增类型时，只扩展工厂，调用方代码尽量不变。
- 配置驱动创建对象，例如 `model_provider=openai`、`retriever_type=bm25`。

### 3. TypeScript 示例

```ts
// 简单工厂：根据类型创建不同的支付渠道
interface PaymentChannel {
  pay(amount: number): void;
}

class AlipayChannel implements PaymentChannel {
  pay(amount: number) {
    console.log(`支付宝支付 ${amount} 元`);
  }
}

class WechatChannel implements PaymentChannel {
  pay(amount: number) {
    console.log(`微信支付 ${amount} 元`);
  }
}

class PaymentFactory {
  static create(type: "alipay" | "wechat"): PaymentChannel {
    switch (type) {
      case "alipay":
        return new AlipayChannel();
      case "wechat":
        return new WechatChannel();
      default:
        throw new Error(`Unsupported channel: ${type}`);
    }
  }
}

// 使用
const channel = PaymentFactory.create("alipay");
channel.pay(100);
```

### 4. 在 Agent 工程里的例子

```text
create_llm(provider)
create_retriever(type)
create_tool(name)
create_skill(skill_id)
```

例如同一个课程代码可以根据环境变量选择 mock 模型或真实 LLM，这就是工厂思想：

```text
调用方只说“我要一个模型”
工厂负责判断“返回 MockLLM、OpenAI ChatModel 还是本地模型”
```

### 5. 优势

- 调用方不依赖具体实现类。
- 新增类型时改动集中。
- 便于测试，用 mock 替换真实实现。
- 便于配置化和插件化。

### 6. 风险

- 简单场景滥用工厂会让代码变绕。
- 工厂容易膨胀成“大杂烩”，需要按领域拆分。
- 如果新增类型还要频繁修改 `switch`，可以进一步升级为注册表模式。

## 二、发布订阅模式

### 1. 核心思想

发布订阅模式让发布者和订阅者通过事件中心解耦。发布者不直接调用订阅者，双方互不感知。

一句话：

> 发布订阅模式解决“模块之间直接依赖”的问题。

### 2. 适用场景

- 跨模块通信。
- 异步事件通知。
- 微前端或插件体系通信。
- 日志、监控、审计、告警。
- Agent 执行过程中的事件流。

### 3. TypeScript 示例

```ts
class EventBus {
  private events: Map<string, Set<Function>> = new Map();

  on(event: string, handler: Function) {
    if (!this.events.has(event)) this.events.set(event, new Set());
    this.events.get(event)!.add(handler);
  }

  off(event: string, handler: Function) {
    this.events.get(event)?.delete(handler);
  }

  emit(event: string, ...args: any[]) {
    this.events.get(event)?.forEach(handler => handler(...args));
  }
}

// 使用：订单模块发布，积分模块订阅
const bus = new EventBus();

bus.on("order:paid", (orderId: string, amount: number) => {
  console.log(`订单 ${orderId} 已支付，增加 ${amount} 积分`);
});

bus.emit("order:paid", "ORD_001", 200);
```

### 4. 与观察者模式的区别

| 模式 | 关系 | 通信方式 |
| --- | --- | --- |
| 观察者模式 | 目标对象直接持有观察者 | 目标直接通知观察者 |
| 发布订阅模式 | 发布者和订阅者都只依赖事件中心 | 发布者发事件，订阅者监听事件 |

简单说：

- 观察者模式：目标和观察者仍然认识彼此。
- 发布订阅：通过事件中心彻底解耦。

### 5. 在 Agent 工程里的例子

Agent 执行时可以发布事件：

```text
agent:start
tool:called
tool:finished
retriever:hit
llm:token
agent:error
agent:finished
```

不同模块订阅不同事件：

- 日志模块订阅所有事件。
- 成本模块订阅 `llm:token`。
- 监控模块订阅耗时和错误事件。
- 前端订阅 `llm:token` 做流式展示。
- 审计模块订阅高风险工具调用。

这样 Agent 主流程不需要直接依赖日志、监控、前端、审计模块。

### 6. 风险

- 事件名混乱会导致难以维护。
- 异步事件顺序可能不稳定。
- 订阅者过多时，排查副作用困难。
- 需要统一事件 schema 和 trace_id。

## 三、装饰器模式

### 1. 核心思想

装饰器模式是在不修改原有对象或函数的前提下，动态地给它“包一层”来增强功能。

一句话：

> 装饰器模式解决“横切关注点侵入业务代码”的问题。

横切关注点包括：

- 日志记录。
- 权限校验。
- 缓存。
- Loading 状态。
- 性能监控。
- 重试和限流。

### 2. TypeScript 函数装饰示例

```ts
function withLoading<T extends (...args: any[]) => Promise<any>>(fn: T): T {
  return (async (...args: any[]) => {
    showLoading();
    try {
      return await fn(...args);
    } finally {
      hideLoading();
    }
  }) as unknown as T;
}

function withErrorToast<T extends (...args: any[]) => Promise<any>>(fn: T): T {
  return (async (...args: any[]) => {
    try {
      return await fn(...args);
    } catch (e: any) {
      toast.error(e.message);
      throw e;
    }
  }) as unknown as T;
}

// 原始函数只关心业务请求
async function fetchOrder(id: string) {
  return request(`/api/orders/${id}`);
}

// 装饰后：组合多个增强能力
const fetchOrderSafe = withErrorToast(withLoading(fetchOrder));
```

原始函数只做业务：

```text
fetchOrder = 获取订单
```

装饰器负责横切能力：

```text
withLoading = Loading 状态
withErrorToast = 错误提示
```

### 3. TypeScript / ES 装饰器语法糖

```ts
function Log(target: any, key: string, desc: PropertyDescriptor) {
  const original = desc.value;
  desc.value = function (...args: any[]) {
    console.log(`[${key}] called with`, args);
    return original.apply(this, args);
  };
}

class OrderService {
  @Log
  createOrder(data: any) {
    // ...
  }
}
```

### 4. 在 Agent 工程里的例子

对工具函数加装饰器：

```text
with_logging(tool)
with_timeout(tool)
with_retry(tool)
with_permission_check(tool)
with_cost_tracking(tool)
```

组合后：

```text
safe_tool = with_cost_tracking(
  with_logging(
    with_retry(
      with_permission_check(raw_tool)
    )
  )
)
```

这和 L10 Skill 里的安全、审计、重试、授权设计高度相关。

### 5. 优势

- 横切关注点和业务逻辑分离。
- 可以自由组合。
- 原始函数更纯粹、更容易测试。
- 增强能力可以复用。

### 6. 风险

- 装饰器层数太多时，调用链不直观。
- 包装顺序会影响行为，例如先鉴权还是先缓存。
- 异常处理需要统一，否则错误可能被吞掉。
- 需要日志或 trace 帮助排查。

## 四、桥接模式

### 1. 核心思想

桥接模式把“抽象”和“实现”分离，让它们可以独立变化。

当一个类存在两个或多个独立变化维度时，用组合代替继承，避免类爆炸。

一句话：

> 桥接模式解决“多维度变化导致类爆炸”的问题。

### 2. 适用场景

- 多维度变化的 UI 组件，例如主题 x 尺寸。
- 跨平台渲染。
- 消息通知，例如渠道 x 消息类型。
- Agent 能力抽象 x 后端实现。
- Retriever 抽象 x 索引后端。

### 3. 没有桥接时的问题

假设要画不同形状，每种形状可以用不同颜色渲染：

```text
Shape
├── RedCircle
├── BlueCircle
├── RedSquare
└── BlueSquare
```

2 种形状 x 2 种颜色 = 4 个类。

如果再加绿色、矩形，就会变成：

```text
3 种形状 x 3 种颜色 = 9 个类
```

这就是类爆炸。

### 4. 桥接后的设计

拆成两个维度：

```text
形状（抽象层）          颜色（实现层）
Circle             x    Red
Square                  Blue
Rectangle               Green
```

形状持有颜色的引用，画的时候委托颜色去上色。

### 5. TypeScript 示例

```ts
// ---------- 实现层：颜色 ----------
interface Color {
  fill(): string;
}

class Red implements Color {
  fill() {
    return "red";
  }
}

class Blue implements Color {
  fill() {
    return "blue";
  }
}

// ---------- 抽象层：形状 ----------
abstract class Shape {
  // 这就是“桥”：形状持有颜色的引用
  constructor(protected color: Color) {}
  abstract draw(): string;
}

class Circle extends Shape {
  draw() {
    return `画一个 ${this.color.fill()} 的圆形`;
  }
}

class Square extends Shape {
  draw() {
    return `画一个 ${this.color.fill()} 的方形`;
  }
}

// 使用：自由组合
new Circle(new Red()).draw();   // 画一个 red 的圆形
new Square(new Blue()).draw();  // 画一个 blue 的方形
```

为什么叫“桥接”？

```text
┌─────────────┐         ┌─────────────┐
│  Shape      │ --桥--> │  Color      │
│  抽象层      │         │  实现层      │
└─────────────┘         └─────────────┘
       │                        │
 Circle / Square          Red / Blue / Green
```

中间那条 `protected color` 引用就是桥。它把两侧连起来，但两侧可以各自独立扩展。

### 6. 在 Agent 工程里的例子

桥接模式非常适合解释 Agent 系统里的“抽象能力 x 具体实现”。

#### 模型桥接

```text
ChatModel 抽象
  x OpenAI 实现
  x 本地模型实现
  x Mock 模型实现
```

#### 检索桥接

```text
Retriever 抽象
  x BM25 实现
  x 向量库实现
  x SQL 实现
  x 多库路由实现
```

#### 通知桥接

```text
Notification 抽象
  x Email 实现
  x 飞书实现
  x Slack 实现
```

它们共同点是：调用方依赖抽象接口，具体实现可以替换。

### 7. 总结口诀

当你发现一个类有两个“轴”在变化：

```text
A x B 导致类爆炸
```

就把其中一个轴抽成接口注入进来，用组合代替继承。

## 五、四种模式对比

| 模式 | 解决的核心问题 | 关键手段 | Agent 工程中的例子 |
| --- | --- | --- | --- |
| 工厂 | 创建逻辑与使用逻辑耦合 | 封装 `new` 操作 | 根据配置创建模型、工具、Skill |
| 发布订阅 | 模块间直接依赖 | 事件中心中介 | 工具事件、日志、监控、SSE |
| 装饰器 | 横切关注点侵入业务代码 | 函数/类包装增强 | 给工具加日志、权限、重试、成本统计 |
| 桥接 | 多维度变化导致类爆炸 | 组合代替继承 | Agent 抽象能力桥接不同模型/检索后端 |

## 六、选择建议

- 创建对象复杂、实现类型多：优先想工厂。
- 模块之间互相通知但不想直接依赖：优先想发布订阅。
- 想给现有函数加日志、权限、缓存、重试：优先想装饰器。
- 两个维度都在变化，继承类越来越多：优先想桥接。

## 七、面试表达

如果被问“工厂模式解决什么问题”：

> 工厂模式把对象创建逻辑封装起来，调用方只依赖统一接口，不关心具体类如何实例化。它适合创建逻辑复杂、需要根据配置动态选择实现的场景。

如果被问“发布订阅和观察者有什么区别”：

> 观察者模式里目标对象直接通知观察者，双方仍然有关联；发布订阅模式通过事件中心解耦，发布者和订阅者互不感知。

如果被问“装饰器模式有什么价值”：

> 装饰器模式在不修改原函数或对象的前提下增强能力，适合日志、权限、缓存、重试等横切关注点，让业务逻辑保持干净。

如果被问“桥接模式什么时候用”：

> 当系统有两个或多个独立变化维度，继承会导致类爆炸时，用桥接模式把抽象和实现分离，通过组合连接两侧，让它们独立扩展。
