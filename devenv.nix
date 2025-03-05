{ pkgs, lib, config, inputs, ... }:

{
  # https://devenv.sh/basics/
  env.DEFAULT_KMS_ARN = "alias/staging-dev-key";
  env.AWS_REGION = "us-west-2";

  # https://devenv.sh/packages/
  packages = [
    pkgs.git
    pkgs.awscli
    pkgs.awsebcli

    pkgs.mypy
    pkgs.nil
    pkgs.python3Packages.python-lsp-server
    pkgs.pulumi-bin
  ];

  # https://devenv.sh/languages/
  languages.python.enable = true;
  languages.python.venv.enable = true;
  languages.python.venv.requirements = ''
    pulumi>=3.153.0,<4.0.0
    pulumi-aws>=6.70.0,<7.0.0
  '';
  # languages.python.poetry.enable = true;
  # languages.python.poetry.install.enable = false;

  # https://devenv.sh/processes/
  # processes.cargo-watch.exec = "cargo-watch";

  # https://devenv.sh/services/
  # services.postgres.enable = true;

  # https://devenv.sh/scripts/
  # scripts.hello.exec = ''
  #   echo hello from $GREET
  # '';
  scripts.kms-encrypt.exec = ''
    INFILE=$1
    KMS_ARN=$2
    if [ -z "$INFILE" ]; then
      INFILE=/dev/stdin
    fi
    if [ -z "$KMS_ARN" ]; then
      KMS_ARN=$DEFAULT_KMS_ARN
    fi
    aws kms encrypt \
      --key-id $KMS_ARN \
      --plaintext fileb://$INFILE \
      --output text \
      --region $AWS_REGION \
      --query CiphertextBlob
  '';
  scripts.kms-encrypt.package = pkgs.bash;


  scripts.kms-decrypt.exec = ''
    INFILE=$1
    KMS_ARN=$2
    if [ -z "$INFILE" ]; then
      INFILE=/dev/stdin
    fi
    if [ -z "$KMS_ARN" ]; then
      KMS_ARN=$DEFAULT_KMS_ARN
    fi
    base64 --decode $INFILE | \
      aws kms decrypt \
        --key-id $KMS_ARN \
        --ciphertext-blob fileb:///dev/stdin \
        --output text\
        --region $AWS_REGION\
        --query Plaintext | \
      base64 --decode
  '';
  scripts.kms-decrypt.package = pkgs.bash;

  scripts.kms-create-alias.exec = ''
    ARN_ID=$1
    ARN_ALIAS=$2
    if [ -z "$ARN_ID" ] || [ -z "$ARN_ALIAS" ]; then
      echo "Usage: kms-create-alias id alias"
    fi
    aws kms create-alias \
      --alias-name $ARN_ALIAS \
      --target-key-id $ARN_ID \
      --region $AWS_REGION
  '';
  scripts.kms-create-alias.package= pkgs.bash;
  
  # enterShell = ''
  #   hello
  #   git --version
  # '';

  # https://devenv.sh/tasks/
  # tasks = {
  #   "myproj:setup".exec = "mytool build";
  #   "devenv:enterShell".after = [ "myproj:setup" ];
  # };

  # https://devenv.sh/tests/
  # enterTest = ''
  #   echo "Running tests"
  #   git --version | grep --color=auto "${pkgs.git.version}"
  # '';

  # https://devenv.sh/git-hooks/
  # git-hooks.hooks.shellcheck.enable = true;

  # See full reference at https://devenv.sh/reference/options/
}
