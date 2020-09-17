# 清华大学学生宿舍电量和热水查询及提醒Bot


## 功能说明

本脚本可以实现以下功能：
1. 定时查询宿舍电量和热水的余量
2. 当电量和热水余量较低时，自动发邮件提醒


## 用法

1. git clone项目到本地，将`config.py.sample`复制到`config.py`
    ```bash
    git clone https://github.com/yaox12/thu-check-electricity-and-water-meters.git
    cd thu-check-electricity-and-water-meters
    cp config.py.sample config.py
    ```
2. 修改`config.py`中的配置
3. 运行
    ```bash
    python3 main.py
    ```
    或设置crontab定时任务（以`/etc/crontab`为例，每天上午9点定时运行）
    ```
    0 9 * * * nobody cd /path/to/dir && python3 main.py >> log.txt
    ```

## To Do

- [ ] 发送邮件时附上最近30天的电量和热水用量曲线图
