# ava-compute


### Setting Up An AWS Instance

[Link To Tutorial](https://aws.amazon.com/getting-started/tutorials/launch-a-virtual-machine/?trk=gs_card&e=gs&p=gsrchttps://aws.amazon.com/getting-started/tutorials/launch-a-virtual-machine/?trk=gs_card&e=gs&p=gsrchttps://aws.amazon.com/getting-started/tutorials/launch-a-virtual-machine/?trk=gs_card&e=gs&p=gsrc)

TL;DR
1. You need to get a SSH key for the instance in the account.
2. You need to add it to `~/.ssh/ava-key-pair.pem`
3. Run `chmod 400 ~/.ssh/ava-key-pair.pem` to make sure it's not publicly viewable
4. Connect to the instance via SSH. You need to fill in `{full path of your .pem file with your path from 3}` and add the IP address from the instance dashboard.
   * Run `ssh -i {full path of your .pem file} ec2-user@{instance IP address}`
   * Optional: Enable X Window client here by adding the `-x` flag.

### Running Code

1. Create a virtualenv.
2. `pip install -r requirements.txt`
3. Add X-ListenApi-Key to your environment variables.
