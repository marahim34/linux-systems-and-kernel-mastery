5. Back to enforcing once the profile is fixed.

Writing a profile for your own service





sudo apt install apparmor-utils
sudo aa-genprof /opt/goodo/venv/bin/uvicorn
# exercise the app fully in another terminal, then (S)can, answer prompts, (F)inish
# result: /etc/apparmor.d/opt.goodo.venv.bin.uvicorn
/opt/goodo/venv/bin/uvicorn {
#include <abstractions/base>
#include <abstractions/python>
/opt/goodo/backend/** r,
/opt/goodo/backend/uploads/** rw,
network inet stream,
}