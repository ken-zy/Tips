---
title: "Swift利用协议实现前缀功能"
date: 2021-07-01
tags: [swift]
draft: false
---

- [Swift利用协议实现前缀功能](#swift利用协议实现前缀功能)
  - [想要实现的功能](#想要实现的功能)
  - [存在的问题](#存在的问题)
  - [解决方案](#解决方案)
    - [属性前增加前缀（不优雅）](#属性前增加前缀不优雅)
    - [点语法增加前缀](#点语法增加前缀)
      - [一、持有属性方式](#一持有属性方式)
      - [二、使用范型](#二使用范型)
        - [给String扩充类型方法](#给string扩充类型方法)
      - [三、利用协议实现前缀](#三利用协议实现前缀)

# Swift利用协议实现前缀功能
## 想要实现的功能
计算字符串中数字的个数
```swift
var greeting = "1234-Hello, playground-1234"
extension String {
    var numberCount: Int {
        var number = 0
        for c in self where ("0"..."9").contains(c){
            number += 1
        }
        return number
    }
}
print(greeting.numberCount)
```
## 存在的问题
直接给一个类增加扩展，容易导致冲突。
## 解决方案
### 属性前增加前缀（不优雅）
```swift
var greeting = "1234-Hello, playground-1234"
extension String {
    var zy_numberCount: Int {
        var number = 0
        for c in self where ("0"..."9").contains(c){
            number += 1
        }
        return number
    }
}
print(greeting.zy_numberCount)
``` 
### 点语法增加前缀
```swift
print(greeting.zy.numberCount)
```
#### 一、持有属性方式
1. 结构体ZY持有str，并在构造方法中初始化
2. 字符串扩展持有zy计算属性

缺点：
1. 不灵活，比如无法给数组扩展功能
```swift
var greeting = "1234-Hello, playground-1234"
struct ZY {
    var str: String
    init(_ str: String) {
        self.str = str
    }
    var numberCount: Int {
        var number = 0
        for c in str where ("0"..."9").contains(c){
            number += 1
        }
        return number
    }
    
    func test() {
        print("---test---")
    }
}

extension String {
    var zy: ZY { ZY(self) }
}

print(greeting.zy.numberCount)
greeting.zy.test()
```

#### 二、使用范型
缺点：使用繁琐，需要给每一个类扩充功能
```swift
var greeting = "1234-Hello, playground-1234"

struct ZY<Base> {
    var base: Base
    init(_ base: Base) {
        self.base = base
    }
}

extension String {
    var zy: ZY<String> { ZY(self) }
}

class People {}
extension People {
    var zy: ZY<People> { ZY(self) }
}

extension ZY where Base == String {
    var numberCount: Int {
        var number = 0
        for c in base where ("0"..."9").contains(c){
            number += 1
        }
        return number
    }
    
    func test() {
        print("---test---")
    }
}

extension ZY where Base: People {
    func run()  {
        print("person run")
    }
}

print(greeting.zy.numberCount)
greeting.zy.test()

var person = People()
person.zy.run()
```

##### 给String扩充类型方法
```swift
struct ZY<Base> {
    var base: Base
    init(_ base: Base) {
        self.base = base
    }
}

extension String {
    var zy: ZY<String> { ZY(self) }
    static var zy: ZY<String>.Type { ZY<String>.self }
}

extension ZY where Base == String {
    var numberCount: Int {
        var number = 0
        for c in base where ("0"..."9").contains(c){
            number += 1
        }
        return number
    }
    
    func test() {
        print("---test---")
    }
    
    static func staticTest() {
        print("---static test---")
    }
}

String.zy.staticTest()
```
#### 三、利用协议实现前缀
```swift
var greeting = "1234-Hello, playground-1234"

/// 前缀类型
struct ZY<Base> {
    var base: Base
    init(_ base: Base) {
        self.base = base
    }
}

/// 利用协议扩展前缀属性
protocol ZYCompatible {}
extension ZYCompatible {
    var zy: ZY<Self> {
        set {} // 使mutating方法编译通过
        get { ZY(self) }
    }
    static var zy: ZY<Self>.Type {
        set {} // 使mutating方法编译通过
        get { ZY<Self>.self }
    }
}

/// 给字符串扩展功能
/// 让 String 拥有 zy 前缀属性
extension String: ZYCompatible {}

/// 给string.zy、String( ).zy前缀扩展功能
extension ZY where Base == String {
    var numberCount: Int {
        var number = 0
        for c in base where ("0"..."9").contains(c){
            number += 1
        }
        return number
    }
    
    mutating func test() {
        print("---test---")
    }
    
    static func staticTest() {
        print("---static test---")
    }
}

print(greeting.zy.numberCount)
greeting.zy.test()

String.zy.staticTest()
```