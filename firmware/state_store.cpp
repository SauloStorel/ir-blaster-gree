#include "state_store.h"

#include <Preferences.h>

namespace {
constexpr char kNamespace[] = "ac";
constexpr char kKey[] = "state";
}  // namespace

AcState loadState() {
  Preferences prefs;
  prefs.begin(kNamespace, true);

  AcState state;
  const size_t read = prefs.getBytes(kKey, &state, sizeof(state));
  prefs.end();

  return read == sizeof(state) ? state : AcState{};
}

void saveState(const AcState& state) {
  Preferences prefs;
  prefs.begin(kNamespace, false);
  prefs.putBytes(kKey, &state, sizeof(state));
  prefs.end();
}
