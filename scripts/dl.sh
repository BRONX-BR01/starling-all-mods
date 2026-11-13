#!/usr/bin/env bash
# baixa result-bNNN um a um; pula os ja baixados; tenta ate 4 vezes
run=${1:?id do run}
mkdir -p ~/r/res
for i in $(seq 0 137); do
  n=$(printf 'b%03d' "$i")
  [ -f ~/r/res/result-$n/result.json ] && continue
  for t in 1 2 3 4; do
    gh run download "$run" -n "result-$n" -D ~/r/res/result-$n 2>/dev/null && break
    sleep 2
  done
  [ -f ~/r/res/result-$n/result.json ] || echo "falhou $n"
done
echo "baixados: $(ls ~/r/res | wc -l)"
