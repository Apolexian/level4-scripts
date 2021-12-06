use quic_socket::{QuicClient, QuicSocket};
use tokio;

#[tokio::main]
async fn main() {
    let mut client = QuicClient::new(None);
    let payload = vec![6; 156];
    client.send(payload).await.unwrap();
}
