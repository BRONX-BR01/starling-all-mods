T = "mixins/accurate_block_placement/tick.rs"
EDITS = [
    (T, "point: t.point,", "point: t.point,\n            inside: false,"),
    (T, "game.tick_hit.replace(Some(hit))", "game.tick_hit.replace(Some(Some(hit)))"),
    (T, "game.remote_use();", "game.remote_use(::mod_api::InteractionAttempt::Press);"),
    (T, "game.tick_hit = kept;", "game.tick_hit.set(kept);"),
]
