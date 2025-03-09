
```sh
# in order to generate the python module included:
pulumi package add terraform-provider smallstep/smallstep

# install the smallstep dependency for pulumi
cd $DEVENV_ROOT/private-keygen-example/sdks/smallstep/ && python3 -m pip install . && cd -

# pulumi up..
```


