#!/bin/bash
# LZU Running Helper - 自动运行脚本
# 使用 crontab 配置定时任务

# 项目根目录（请根据实际情况修改）
PROJECT_DIR="/path/to/LZURunningHelper"
PYTHON_BIN="$PROJECT_DIR/.venv/bin/python"

# 日志目录
LOG_DIR="$PROJECT_DIR/logs"
mkdir -p "$LOG_DIR"

# 获取当前日期和时间
DATE=$(date +"%Y-%m-%d")
TIME=$(date +"%H:%M:%S")

# 日志文件
MORNING_LOG="$LOG_DIR/morning_$DATE.log"
EVENING_LOG="$LOG_DIR/evening_$DATE.log"

# 早上任务函数
run_morning() {
    echo "========================================" >> "$MORNING_LOG"
    echo "开始执行早上任务: $DATE $TIME" >> "$MORNING_LOG"
    echo "========================================" >> "$MORNING_LOG"
    
    cd "$PROJECT_DIR" || exit 1
    
    # 执行早上配置
    $PYTHON_BIN main.py -f config.morning.json -a >> "$MORNING_LOG" 2>&1
    
    EXIT_CODE=$?
    
    if [ $EXIT_CODE -eq 0 ]; then
        echo "[SUCCESS] 早上任务执行成功" >> "$MORNING_LOG"
    else
        echo "[ERROR] 早上任务执行失败，退出码: $EXIT_CODE" >> "$MORNING_LOG"
    fi
    
    echo "" >> "$MORNING_LOG"
}

# 晚上任务函数
run_evening() {
    echo "========================================" >> "$EVENING_LOG"
    echo "开始执行晚上任务: $DATE $TIME" >> "$EVENING_LOG"
    echo "========================================" >> "$EVENING_LOG"
    
    cd "$PROJECT_DIR" || exit 1
    
    # 执行晚上配置
    $PYTHON_BIN main.py -f config.evening.json -a >> "$EVENING_LOG" 2>&1
    
    EXIT_CODE=$?
    
    if [ $EXIT_CODE -eq 0 ]; then
        echo "[SUCCESS] 晚上任务执行成功" >> "$EVENING_LOG"
    else
        echo "[ERROR] 晚上任务执行失败，退出码: $EXIT_CODE" >> "$EVENING_LOG"
    fi
    
    echo "" >> "$EVENING_LOG"
}

# 根据参数决定执行哪个任务
case "$1" in
    morning)
        run_morning
        ;;
    evening)
        run_evening
        ;;
    *)
        echo "Usage: $0 {morning|evening}"
        exit 1
        ;;
esac

exit 0
