// main.rs —— 高频信号处理节点（Rust）
// 每次 tick：生成一个正弦波值，放大后发出。
use dora_node_api::{
    self, DoraNode, Event, IntoArrow, dora_core::config::DataId,
};
use eyre::Result;

fn main() -> Result<()> {
    // ① 连线
    let (mut node, mut events) = DoraNode::init_from_env()?;
    let output = DataId::from("value".to_owned());

    let mut step: f32 = 0.0;     // 相位计步器

    // ② 主循环
    while let Some(event) = events.recv() {
        match event {
            // ③ 处理输入事件
            Event::Input { id, metadata, .. } => {
                if id.as_str() == "tick" {
                    // 生成正弦波并放大 10 倍（这就是"高频计算"部分）
                    let signal = (step * 0.1).sin() * 10.0;
                    step += 1.0;

                    // 发送：把 f32 转成 Arrow 发出去
                    node.send_output(
                        output.clone(),
                        metadata.parameters,
                        signal.into_arrow(),
                    )?;
                }
            }
            Event::Stop(_) => break,
            _ => {}
        }
    }

    Ok(())
}
