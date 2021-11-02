use quic_socket::QuicListener;
use tokio;

#[tokio::main]
async fn main() {
    let addr = "0.0.0.0:4442".parse().unwrap();
    let mut listener = QuicListener::new(addr).unwrap();
    listener.accept().unwrap();
    let mut buf = [0; 6553];
    let mut conn = listener.connection.take().unwrap();
    if conn.is_established() {
        for stream_id in conn.readable() {
            while let Ok((read, _)) = conn.stream_recv(stream_id, &mut buf) {
                println!("Got {} bytes on stream {}", read, stream_id);
            }
        }
    }
}
