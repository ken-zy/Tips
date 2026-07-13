---
title: "使用Property Wrapper创建Weak Array"
date: 2022-11-07T16:40:44+08:00
tags: [swift]
draft: false
---

- [Property Wrapper是什么](#property-wrapper是什么)
- [使用Property Wrapper创建Weak Array](#使用property-wrapper创建weak-array)

# Property Wrapper是什么
属性包装器是Swift 5的一项强大功能。
为了更好的了解属性包装器，让我们举一个例子来看一下它们能解决哪些问题。
假如我们想要添加一个日志记录功能，每次属性更改时，我们都会将其新值打印到Xcode控制台。
这样追踪错误或追踪数据流时非常有用。
实现此目的的直接方法是覆盖setter：
```swift
struct Bar {
    private var _x = 0
    var x: Int {
        get { _x }
        set {
            _x = newValue
            print("New value is \(newValue)")
        }
    }
    var bar = Bar()
    bar.x = 1 /// print 'New value is 1'
}
```
如果我们继续记录更多的这样的属性，那么代码很快就会变得一团糟。
为了不用每个新属性一遍又一遍的复制相同代码，我们声明一个新类型，该新类型将执行日志记录：
```swift
struct ConsoleLogged<Value> {
    private var value: Value

    init(wrappedValue: Value) {
        self.value = wrappedValue
    }

    var wrappedValue: Value {
        get { value }
        set {
            value = newValue
            print("New value is \(newValue)")
        }
    }
}
```

这是我们如何使用ConsoleLogged重写Bar的方法：
```swift
struct Bar {
    private var _x = ConsoleLogged<Int>(wrappedValue: 0)

    var x: Int {
        get { _x.wrappedValue }
        set { _x.wrappedValue = newValue }
    }

    var bar = Bar()
    bar.x = 1 /// print 'New value is 1'
}
```

Swift为此模式提供了语言上的支持。 我们需要做的就是将@propertyWrapper属性添加到我们的ConsoleLogged类型中：
```swift
/// 您可以将property wrapper视为常规属性，它将get和set方法委托给其他类型。
@propertyWrapper
struct ConsoleLogged<Value> {
    private var value: Value

    init(wrappedValue: Value) {
        self.value = wrappedValue
    }

    var wrappedValue: Value {
        get { value }
        set {
            value = newValue
            print("New value is \(newValue)")
        }
    }
}
```

在属性声明的地方，我们可以指定哪个包装器实现它：
```swift
/// 属性@ConsoleLogged是一个语法糖，它会转换为我们代码的先前版本。
/// 通过@propertyWrapper可以移除掉一些重复或者类似的代码。
struct Bar {
    @ConsoleLogged var x = 0
}

var bar = Bar()
bar.x = 1 // Prints 'New value is 1'
```

# 使用Property Wrapper创建Weak Array
```swift
import Foundation

final class WeakObject<T: AnyObject> {
    private(set) weak var value: T?
    init(_ value: T) {
        self.value = value
    }
}

@propertyWrapper
public struct WeakArray<Element> where Element: AnyObject {
    private var storage = [WeakObject<Element>]()
    
    public init() {}
    
    public var wrappedValue: [Element] {
        /// compactMap 是对原序列进行遍历，然后解包过滤掉 nil ，然后返回一个新的 non-Optional 序列
        get { storage.compactMap { $0.value } }
        set { storage = newValue.map{ WeakObject($0) } }
    }
}
```
使用：
```swift
@WeakArray private var weakObjs: [String]
```