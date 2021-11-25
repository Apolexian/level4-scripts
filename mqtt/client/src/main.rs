// Adapted from https://github.com/bytebeamio/rumqtt/blob/master/rumqttc/examples/syncpubsub.rs
use rumqttc::{self, Client, LastWill, MqttOptions, QoS};
use std::thread;
use std::time::Duration;
use std::env;

fn main() {
    pretty_env_logger::init();
    let args: Vec<String> = env::args().collect();
    let ip = &args[1];
    let self_addr = "0.0.0.0:1884".parse().unwrap();
    let mut mqttoptions = MqttOptions::new("test-1", ip, 1883, self_addr);
    mqttoptions.set_connection_timeout(10);
    let will = LastWill::new("hello/world", "good bye", QoS::AtMostOnce, false);
    mqttoptions.set_keep_alive(5).set_last_will(will);

    let (client, mut connection) = Client::new(mqttoptions, 10);
    thread::spawn(move || publish(client));

    for (i, notification) in connection.iter().enumerate() {
        println!("{}. Notification = {:?}", i, notification);
    }

    println!("Done with the stream!!");
}

fn publish(mut client: Client) {
    client.subscribe("hello/+/world", QoS::AtMostOnce).unwrap();
    for i in 0..10 {
        let payload = vec![1; i as usize];
        let topic = format!("hello/{}/world", i);
        let qos = QoS::AtLeastOnce;

        client.publish(topic, qos, true, payload).unwrap();
    }

    thread::sleep(Duration::from_secs(5));
}
