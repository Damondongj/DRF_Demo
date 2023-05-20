from confluent_kafka import Consumer, KafkaError

# Kafka 服务器配置
bootstrap_servers = 'localhost:9092'

# 创建 Consumer 实例
consumer = Consumer({
    'bootstrap.servers': bootstrap_servers,
    'group.id': 'your_consumer_group',
    'auto.offset.reset': 'earliest'  # 从最早的可用偏移量开始消费
})

# 订阅主题
topic = 'your_topic'
consumer.subscribe([topic])

# 消费消息
while True:
    msg = consumer.poll(1.0)  # 从消费者获取消息，超时时间为1秒

    if msg is None:
        continue

    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            # 到达分区末尾，继续下一个消息
            continue
        else:
            # 其他错误，处理或中止消费
            print(f"Kafka 错误: {msg.error().str()}")
            break

    # 处理接收到的消息
    print(f"接收到消息: {msg.value().decode('utf-8')}")

# 关闭 Consumer
consumer.close()
