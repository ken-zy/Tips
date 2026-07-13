---
title: "写给iOSer的实践指南 如何快速上手Android项目"
date: 2023-10-10T15:15:21+08:00
tags: [Android]
draft: false
---

- [理解Gradle的各种配置文件](#理解gradle的各种配置文件)
  - [setting.gradle文件](#settinggradle文件)
  - [项目根build.gradle文件](#项目根buildgradle文件)
  - [模块的build.gradle文件](#模块的buildgradle文件)
    - [Plugin](#plugin)
    - [Android](#android)
- [Android四大组件](#android四大组件)
  - [activity](#activity)
  - [service](#service)
  - [content provider](#content-provider)
  - [broadcast receiver](#broadcast-receiver)
- [Intent](#intent)
- [资源管理](#资源管理)
  - [资源目录结构：](#资源目录结构)
  - [配置限定符：](#配置限定符)
  - [资源访问：](#资源访问)

# 理解Gradle的各种配置文件

当Android studio创建新项目时，默认会生成三个Gradle文件。  
其中两个，setting.gradle和build.gradle在项目根目录中。另一个build.gradle在应用程序模块中。  
如下所示  

```
MyApp
  | - build.gradle
  | - setting.gradle
  | - app
```

这三个文件每一个都有其独有的用处。  

## setting.gradle文件  
setting文件在Build初始化阶段执行，定义了哪些模块应改被包含在构建中。  
单个模块项目不一定需要setting文件，但是多模块项目必须要包含setting文件；否则，Gradle不知道要将哪些模块包含到构建中。  

`include ':app'`

如上所示：app模块被包含其中。  

## 项目根build.gradle文件  
在项目根目录的build.gradle文件中，你可以配置需要应用于项目中所有模块的选项。它默认包含两个代码块：  

```c
buildscript {
    repositories {
        jcenter()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:1.2.3'
    }
}
allprojects {
    repositories {
        jcenter()
    }
}
```

buildscript代码块是配置实际构建的位置。  



在**repositories{...}**代码块中，可以看到我们在 repositories{} 中将JCenter配置为依赖库。  

依赖库意味着依赖的来源，或者换句话说，一个可下载的第三方库列表，我们可以在我们的应用和库中使用。  

JCenter是一个Gradle预先内置的Maven存储库，Gradle默认已经配置好相关了，不需要你额外的设置 。  

Gradle中还有几个内置的存储库，并且Gradle也支持添加自己的本地或远程仓库。  



构建脚本**dependencies{...}**代码块中还定义了对Android build tools的依赖，这个依赖就是Android插件。  



dependencies{} 用于为构建过程本身配置依赖。  

这意味着你不应在顶级构建文件中包含你的应用程序或库所需的依赖关系。  
  
当前默认定义了唯一的一个依赖是Gradle的Android插件。  

Android插件是每个Android模块构建所必须的，因为这个插件定义了Android程序的具体构建流程，包含了可以执行的Android相关任务。  





allprojects{} 可用于定义需要应用于所有模块的属性。你可以在allprojects{}创建任务，那么这些任务将在所有模块中都可用。  

因为allprojects是将其中的配置应用到所有模块中，如果不是公共的通用配置，而是单独于某一个模块中的配置，最好是放在模块中的build文件中。  

## 模块的build.gradle文件  
模块级的build.gradle文件包含仅适用于Android应用程序或库模块的选项。  

它可以直接覆盖顶级build.gradle文件中的任何配置选项。

模块build.gradle文件内容如下所示：

```
apply plugin: 'com.android.application'
android {
       compileSdkVersion 22
       buildToolsVersion "22.0.1"
       defaultConfig {
           applicationId "com.gradleforandroid.gettingstarted"
           minSdkVersion 14
           targetSdkVersion 22
           versionCode 1
           versionName "1.0"
   }
 
  buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile
            ('proguard-android.txt'), 'proguard-rules.pro'
        }
   }
}
 
dependencies {
    compile fileTree(dir: 'libs', include: ['*.jar'])
    compile 'com.android.support:appcompat-v7:22.2.0'
}
```
### Plugin
第一行代码应用Android应用程序插件，在前面我们介绍过，Android插件被项目根构建文件配置为build过程的依赖。

Android插件提供构建，测试和打包Android应用程序和库所需的所有任务,现由Google Android Tools Team编写和维护。

### Android
构建文件的最大部分是android块。 此块包含整个Android特定的构建配置。

android配置块中至少需要配置属性是compileSdkVersion和buildToolsVersion：



compileSdkVersion:编译Android程序的sdk版本
buildToolsVersion：编译过程中使用的android构建工具的版本
defaultConfig配置了应用程序的核心属性。

此块中的属性将覆盖AndroidManifest.xml文件中的相应条目：

此块中的第一个属性是applicationId。

这将覆盖manifest文件中的包名称，但applicationId和应用包名之间有一些差异。

在Gradle用作默认Android构建系统之前，AndroidManifest.xml中的包名称有两个目的：

一是用作应用程序的唯一标识符，

再就是用作R资源类中包的名称。

假设有如下场景：你要发布一款app，有一个免费版本和付费版本。

并且这两个版本需要具有单独的标识符，

因为它们在Google Play商店中需要显示为不同的应用，并且可以同时安装。

然而，在未使用Gradle构建之前，源代码和生成的R类必须始终保持相同的包名称，因此，在创建不同的版本时，所有的源文件将需要更改。

在使用Gradle之后applicationId和包名区分开了，这样你可以随意更改项目的应用Id而不必更改源码的包名。

manifest文件中定义的程序包名继续在源代码和R类中使用，而设备和Google Play使用applicationId作为唯一标识符。

defaultConfig中接下来的两个属性是minSdkVersion和targetSdkVersion。

这两个应该看起来很熟悉，因为它们在manifest文件中被定义为元素的一部分。

minSdkVersion设置用于配置运行应用程序所需的最低API级别。

targetSdkVersion设置通知系统该应用程序在特定版本的Android上测试，并且操作系统不需要启用任何向前兼容性行为。这与我们之前看到的compileSdkVersion无关。

versionCode和versionName也具有与manifest文件中相同的功能，并为您的应用定义版本号和用户友好的版本名称。

构建文件中的所有值都将覆盖清单文件中的值。因此，如果在build.gradle中定义它们，则不需要在清单文件中定义它们。如果构建文件不包含值，则使用manifest文件中定义的值。

buildTypes块是你定义如何构建和打包应用程序的不同构建类型(Debug或者Release)的地方。

Dependencies
依赖块是标准Gradle配置的一部分（这也是为什么它放在了android块之外），并定义了应用模块或库模块的所有依赖关系。

默认情况下，新的Android应用程序依赖于libs目录中的所有JAR文件和相应的support包下的库。



# Android四大组件
## activity
定义：Activity代表了用户界面的一个单独的屏幕。每个Activity都提供了一个与用户互动的界面。

生命周期：Activity有其自己的生命周期，从创建到销毁，包括多个状态，如onCreate(), onStart(), onResume(), onPause(), onStop(), onDestroy()等。

用途：用于展示用户界面和与用户交互。

## service
定义：Service是一个在后台运行的组件，用于执行长时间运行的操作或远程进程。它没有用户界面。

生命周期：Service有其自己的生命周期方法，如onCreate(), onStartCommand(), onBind(), onUnbind(), onDestroy()等。

用途：用于执行后台任务，如下载文件、播放音乐等。

## content provider
定义：Content Provider是一个组件，用于管理应用之间的数据共享。它提供了一套标准的API，用于查询和修改数据。

生命周期：Content Provider没有像Activity或Service那样的明确的生命周期。它在需要时创建，并在不再需要时销毁。

用途：用于共享数据，如联系人、照片、设置等。

## broadcast receiver
定义：Broadcast Receiver是一个组件，用于接收和响应应用外部的广播消息。

生命周期：Broadcast Receiver的生命周期非常短。当接收到一个广播时，onReceive()方法会被调用，该方法执行完毕后，Broadcast Receiver就会被销毁。

用途：用于响应系统或应用发出的广播，如电池电量低、屏幕关闭、网络状态变化等。

# Intent
Intent是Android系统用来抽象描述要执行的一个操作，也可以在不同组件之间进行沟通和消息传递。

显式的Intent就是你已经知道要启动的组件名称，比如某个Activity的包名和类名，在Intent中明确的指定了这个组件(Activity)，一般来说这种Intent经常用在一个应用中，因为你已经明确的知道要启动的组件名称。

```
Intent intent = new Intent(this, TargetActivity.class);
startActivity(intent);
```


隐式的Intent就是你不知道要启动的组件名称，只知道一个Intent动作要执行，比如：拍照，录像，查看地图。一般来说这种Intent用在不同的应用之间传递信息。

```
Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse("http://www.google.com"));
startActivity(intent);
```

# 资源管理
在Android开发中，资源管理是一个核心概念。

资源是那些非代码部分的应用组件，如图像、字符串、布局和样式。

Android提供了一个强大的资源管理系统，允许开发者为不同的设备配置、屏幕尺寸和语言提供适当的资源。

以下是Android资源管理的详细解释：

## 资源目录结构：
在Android项目中，所有的资源文件都存放在 res/ 目录下。这个目录包含了多个子目录，每个子目录都对应一种资源类型：

- drawable/：图像文件（如PNG、JPEG、GIF）或XML描述的图形。
- layout/：XML描述的UI布局。
- values/：包含XML文件，如字符串、颜色、尺寸和样式定义。
- mipmap/：应用图标。
- menu/：XML描述的应用菜单。
- raw/：任何需要原封不动保存的文件，如音频文件。
- xml/：其他的XML配置文件。
## 配置限定符：
可以为特定的设备配置或条件提供特定的资源。

这是通过在资源目录名称中添加配置限定符来实现的。例如：

- values-zh/：为中文提供的字符串。
- layout-land/：为横屏提供的布局。
- drawable-hdpi/：为高密度屏幕提供的图像。
## 资源访问：
在代码中，可以使用自动生成的 R 类来访问资源。例如：

```
String appName = getString(R.string.app_name);
Drawable icon = getResources().getDrawable(R.drawable.icon);
```
在XML中，可以使用 @ 符号来引用资源。例如：

```
<TextView
    android:text="@string/hello_world"
    android:background="@drawable/background" />
```
资源值文件：
在 values/ 目录下，可以定义多种资源值：

- strings.xml：字符串值。
- colors.xml：颜色值。
- dimens.xml：尺寸值。
- styles.xml：样式和主题。



