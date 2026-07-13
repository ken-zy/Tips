---
title: "Swift中的属性"
date: 2021-06-17
tags: [swift]
draft: false
---
   * [Swift 中的属性](#swift-中的属性)
      * [实例属性](#实例属性)
         * [存储属性](#存储属性)
         * [计算属性](#计算属性)
         * [Example](#example)
         * [枚举 rawValue 原理](#枚举-rawvalue-原理)
         * [延迟存储属性（Lazy Stored Property）](#延迟存储属性lazy-stored-property)
         * [属性观察器（Property Observe）](#属性观察器property-observe)
         * [全局变量，局部变量](#全局变量局部变量)
         * [inout 的再次研究](#inout-的再次研究)
      * [类型属性 （Type Property）](#类型属性-type-property)
         * [类型属性细节](#类型属性细节)
         * [单例模式](#单例模式)
      * [协议中的属性](#协议中的属性)

# Swift 中的属性
## 实例属性
### 存储属性
1. 类似成员变量的概念
2. 存储在实例的内存中
3. 结构体、类可以定义存储属性 ✅
4. 枚举不可以定义存储属性 ❎
5. 在创建类或结构体实例的时候，必须为所有实例属性设置一个合适的初始值
   1. 可以在初始化器里为存储属性设置一个初始值
   2. 可以分配一个默认的属性值作为属性定义的一部分
### 计算属性
1. 本质就是方法（函数）
2. 不占用实例的内存
3. 枚举、结构体、类都可以定义计算属性
4. set 传入的新值默认叫做 newValue，也可以自定义
   -  ```swift
      struct Circle {
          var radius: Double
          var diameter: Double {
              set (newDiameter) {
                  radius = newDiameter / 2
              }
              get {
                  radius * 2
              }
          }
      }
      ```
5. 定义计算属性只能用 var，不能用 let
    - let 代表常量，值是一成不变的
    - 计算属性的值是可能发生变化的（即使是只读计算属性）
      - 上述例子中的 radius 改变会导致 diameter 变化
6. 只读计算属性：只有 get，没有 set
   - ```swift
     struct Circle {
         var radius: Double
         var diameter: Double { radius * 2 }
     }
     ```

### Example
```swift
struct Circle {
    // 存储属性
    var radius: Double
    // 计算属性
    var diameter: Double {
        set {
            radius = newValue / 2
        }
        get {
            radius * 2
        }
    }
}
var circle = Circle(radius: 5)
print(circle.radius) // 5.0
print(circle.diameter) // 10.0
circle.diameter = 12
print(circle.radius) // 6.0
print(circle.diameter) // 12.0
```
### 枚举 rawValue 原理
1. 枚举 rawValue 的本质是只读计算属性
   ```swift
   enum TestEnum: Int {
       case test1 = 1, test2 = 2, test3 = 3
       var rawValue: Int {
           Switch Self {
               case .test1:
                    return 10
               case .test2:
                    return 11
               case .test3:
                    return 12
           }
       }
   }
   print(TestEnum.test3.rawValue) // 12
   ``` 
### 延迟存储属性（Lazy Stored Property）
使用 lazy 可以定义一个延迟存储属性，在第一次用到属性的时候才会进行初始化
- lazy 属性必须是 var，不能是 let
  - let 必须在实例的初始化方法完成之前就拥有值
- 如果多条线程同时第一次访问 lazy 属性，无法保证属性只能被初始化一次
- 当结构体包含一个延迟存储属性时，只有 var 才能访问延迟存储属性
  - 因为延迟存储属性初始化时会改变结构体内存
  - ```swift
    struct Point {
        var x = 0
        var y = 0
        lazy var z = 0
    }
    let p = Point()
    print(p.z) // 报错 cannot use mutating getter or immutable value
    ```
### 属性观察器（Property Observe）
可以为非 lazy 的 var 存储属性设置属性观察器
- willSet 会传递新值，默认叫 newValue
- didSet 会传递旧值，默认叫 oldValue
- 在初始化器中设置属性值不会触发 wllSet 和 didSet
- 在属性观察器中设置初始值也不会触发 willSet 和 didSet
  ```swift
  struct Circle {
      var radius: Double {
          willSet {
              print("will set", newValue)
          }
          didSet {
              print("did set", oldValue, radius)
          }
      }
      init() {
          self.radius = 1.0
          print("Circle init")
      }
      // Circle init
      var circle = Circle()

      // will set 10.5
      // did set 1.0 10.5
      cricle.radius = 10.5
      // 10.5
      print (circle.radius)
  }
  ```
### 全局变量，局部变量
属性观察器、计算属性功能，同样可以应用在全局变量及局部变量身上

### inout 的再次研究
总结：
1. inout 的本质就是引用传递（地址传递）
2. 如果实参有物理内存地址，且没有设置属性观察器
   - 直接将实参内存地址传入函数（实参进行引用传递） 
3. 如果实参是计算属性或者设置了属性观察器
   - 采用了 copy in copy out 的做法
     - 调用该函数时，先复制实参的值，产生副本 【get】 
     - 将副本的内存地址传入函数（副本进行引用传递），在函数内部可以修改副本的值
     - 函数返回后，再将副本的值覆盖实参的值 【set】
```swift
struct Shape {
    var width: Int
    var side: Int {
        willSet {
            print("will set side", newValue)
        }
        didSet {
            print("did set side", oldValue, side)
        }
    }
    var girth: Int {
        set {
            width = newValue / side
            print("set girth", newValue)
        }
        get {
            print("get girth")
            return width * side
        }
    }
    func show() {
        print("width=\(width), side=\(side), girth=\(girth)")
    }
}

struct Test {
    func test (_ num: inout Int) {
        num = 20
    }
    
    func example() {
        var s = Shape(width: 10, side: 4)
        test(&s.width)
        s.show()
        print("----------")
        test(&s.side)
        s.show()
        print("----------")
        test(&s.girth)
        s.show()
        print("----------")
    }
}

var test = Test()
test.example()

// get girth
// width=20, side=4, girth=80
// ----------
// will set side 20
// did set side 4 20
// get girth
// width=20, side=20, girth=400
// ----------
// get girth
// set girth 20
// get girth
// width=1, side=20, girth=20
// ----------
```
## 类型属性 （Type Property）
严格来说，属性可以分为：
- 实例属性（Instance Property）：只能通过实例去访问
  - 存储实例属性（Stored Instance Property），存储在实例内存中，每个实例一份
  - 计算实例属性（Computed Instance Property）
- 类型属性（Type Property）：只能通过类型去访问
  - 存储类型属性（Stored Type Property）：整个程序运行过程中，就只有一份内存
  - 计算类型属性（Computed Type Property）

- 可以通过 `static` 定义类型属性
- 如果是类，也可以用 `class`
```swift
struct Car {
    static var count: Int = 0
    init() {
        Car.count += 1
    }
}
let c1 = Car()
let c2 = Car()
let c3 = Car()
print(Car.count) // 3
``` 
### 类型属性细节
- 不同于存储实例属性，你必须给存储类型属性设定初始值
  - 因为类型没有像实例那样的`init()`初始化器来初始化存储属性
- 存储类型属性默认就是 lazy，会在第一次使用时初始化
  - 就算被多个线程同时访问，保证只初始化一次
  - 存储类型属性可以是 let
- 枚举类型也可以定义类型属性（存储类型属性，计算类型属性）

### 单例模式
init 方法要隐藏，避免外部访问
```swift
public struct FileManager {
    public static let shared = FileManager()
    private init() {}
}

public struct FileManager {
    public static let shared = {
        // ...
        // ...
        return FileManager()
    }()
    private init() {}
}
```

## 协议中的属性
```swift
protocol Drawable {
    func draw()
    var x: Int {set get}
    var y: Int {get}
    subscript(index: Int) -> Int {get set}
}
```

1. 协议中定义的属性必须使用 var 关键字
2. 实现协议时的属性权限要不小于协议中定义的属性权限
   - 协议中规定get、set，用var存储属性或者set，get计算属性实现
   - 协议中定义get，用任何属性都可以实现