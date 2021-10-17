// adapted from https://github.com/bytebeamio/rumqtt/blob/master/rumqttd/examples/broker.rs
use librumqttd::{Broker, Config};
use std::thread;

fn main() {
    pretty_env_logger::init();
    let config: Config = confy::load_path("config/rumqttd.conf").unwrap();
    let mut broker = Broker::new(config);

    let mut tx = broker.link("localclient").unwrap();
    thread::spawn(move || {
        broker.start().unwrap();
    });

    let mut rx = tx.connect(200).unwrap();
    tx.subscribe("#").unwrap();

    // subscribe and publish in a separate thread
    thread::spawn(move || {
        for _ in 0..10 {
            for i in 0..200 {
                let topic = format!("hello/{}/world", i);
                tx.publish(topic, false, vec![0; 1024]).unwrap();
            }
        }
    });

    let mut count = 0;
    loop {
        if let Some(message) = rx.recv().unwrap() {
            count += message.payload.len();
            println!("{}", count);
        }
    }
}
