use quic_socket::QuicListener;
use tokio;
use url::Url;

#[tokio::main]
async fn main() {
    let url = Url::parse("http://127.0.0.1:4442").unwrap();
    let mut payload = [6; 156];
    QuicListener::send(
        "cert.der".to_string(),
        url,
        Some("localhost".to_string()),
        &mut payload,
    )
    .await
    .unwrap();
}
