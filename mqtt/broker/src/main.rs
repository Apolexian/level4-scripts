use librumqttd::{Broker, Config};
use std::thread;

fn main() {
    pretty_env_logger::init();
    let config: Config = confy::load_path("rumqttd.conf").unwrap();
    let mut broker = Broker::new(config);

    let mut tx = broker.link("localclient").unwrap();
    thread::spawn(move || {
        broker.start().unwrap();
    });

    let mut rx = tx.connect(300).unwrap();
    tx.subscribe("#").unwrap();

    thread::spawn(move || {
        for i in 2..4 {
            let topic = format!(
                "GENERICO-CORPO/JSON/0/1/ADDITIVE-MANUFACTURING-1{}/PRINT/1",
                i
            );
            tx.publish(topic, true, "init".as_bytes()).unwrap();
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
