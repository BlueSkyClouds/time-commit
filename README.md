# 自动刷github提交记录


## 前言
进入自己github主页会看到自己的提交记录，如果某天没有提交记录，那天的小方框就显示灰色。强迫症的我，每次进来看着就感觉不爽，
哪天忙了就会忘记提交，所以想着能不能实现在自己阿里云服务器(linux系统)上，设置cron，定制下git命令，实现每天定点自动提交。

## 第一步：克隆我的项目

不同的克隆方式导致校验方式不同，对应的免秘方式也不一样。简单来说，https通过记住账号密码免登，ssh通过校验生成的密钥免登。
  
- 1.https克隆

- 2.ssh克隆


如果，你已经克隆了项目，不知道采用了哪种方式，可以执行：

```bash
git remote -v
```
如果是这样：  

```
origin https://github.com/tywei90/git-auto-commit.git (fetch)  
origin https://github.com/tywei90/git-auto-commit.git (push)  
```
那么就是https方式； 

如果是这样：  

```
origin	git@github.com:tywei90/git-auto-commit.git (fetch)  
origin	git@github.com:tywei90/git-auto-commit.git (push)  
```
那么就是ssh方式。  

更改克隆方式也很简单：  

https ——> ssh  
`git remote set-url origin git@github.com:tywei90/git-auto-commit.git`

ssh ——> https  
`git remote set-url origin https://github.com/tywei90/git-auto-commit.git`

## 第二步：免密登录
如果不做免密登录,每次操作都需要输入用户名和密码.很麻烦.
针对上面两种克隆项目的方式，有两种免密登录设置。

### 1.账号密码免登（https克隆）
```bash
cd time-commit/.git
vim config
```
在config文件最后添加如下代码：

```
[credential]  
    helper = store
```
保存，输入一次账号密码后第二次就会记住账号密码了


或者执行
`git config --global credential.helper store`

当你再次操作的时候,最后输入一次账号和密码就可以了.它会在你的用户目录下生成`.git-credentials`文件.
文件内容为用户名+密码.

### 2.公钥私钥免登（ssh克隆）

#### 2.1 生成公钥和私钥

检查本机的ssh密钥：
```bash
cd ~/.ssh 
ls
```
如果提示：No such file or directory，说明你是第一次使用git，那就自己手动创建目录  

使用ssh-keygen命令生成ssh密钥，命令如下：

```bash
ssh-keygen -t rsa
```
输入上面命令后，遇到选择直接回车，即可生成ssh 密钥。生成ssh 密钥后，可以到~/.ssh目录下查看相关文件，一般来说ssh 密钥会包含id_rsa和id_rsa.pub两个文件，分别表示生成的私钥和公钥。

#### 2.2 拷贝公钥到你的github
在.ssh目录下，执行`cat id_rsa.pub`，复制所有公钥内容

点击github的头像，在下拉菜单中选择 setting 选项，在打开页面的左侧菜单中点击 SSH and GPG keys，然后点击新页面右上角绿色按钮 New SSH key。填写title值，并将复制的公钥内容粘贴到key输入框中提交。

#### 2.3 测试链接github
我看网上是输入如下命令：

```bash
ssh –t git@github.com
```
然后，我的会报ssh: Could not resolve hostname \342\200\223t: Name or service not known的错误，搜了下，解决办法是执行下列命令：

```bash
ssh -t -p 22 git@github.com 
```
-p表示修改服务器端口为22，当提示输入(yes/no)?时在后面输入yes回车即可。但是最后还是报错，后来又搜了下，执行如下代码：
```bash
ssh git@github.com
```
即将`-t`去掉就好了，看到 Hi ** You've successfully authenticated, but GitHub does not provide shell access. 说明连接成功了，大家可以都试一试。

## 第三步：设置cron，定时自动提交任务
cron是一个Linux下的后台进程，用来定期的执行一些任务.    

项目里的add.js是用来修改records.txt的，每次执行会将当前的时间附加到records.txt文件末尾。然后让git自动提交即可。

下面关键是cron的设置，这里直接将cron设置粘贴出来。先执行`crontab -e`进入cron编辑，如果是第一次使用这个命令,系统会让你选择文本编辑器,我选的是vim,第4选项.

选错也没有关系,选定的编辑器也可以使用`select-editor`命令来更改.

然后编辑该文件.

然后粘贴如下代码：

```bash
00 12 * * * cd /home/time-commit && git pull && /root/.nvm/versions/node/v6.6.0/bin/node add.js && git commit -a -m 'git auto commit' && git push origin master 
```
* `00 12 * * *`的意思是，每天的12:00执行后面的命令。  

* `/root/.nvm/versions/node/v6.6.0/bin/node`是node二进制执行文件的绝对路径，不能直接写node命令，不会识别的。如何查出自己的node执行目录，其实很简单，执行`which node`即可。

* `'git auto commit'`是每次提交的comment，可以随意发挥.

保存了crontab之后，我们还需要重启cron来应用这个计划任务。使用以下命令：

```
sudo service cron restart
```

然后服务器就会每天准时帮助你在github上面签到.
