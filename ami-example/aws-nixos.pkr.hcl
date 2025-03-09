variable "region" {
  type = string
  description = "the region where the image will be built"
}

variable "vpc_id" {
  type = string
  description = "the vpc where the image will be built"
}

variable "subnet_id" {
  type = string
  description = "the subnet where the image will be built"
}

packer {
  required_plugins {
    amazon = {
      version = ">= 1.2.8"
      source  = "github.com/hashicorp/amazon"
    }
  }
}

source "amazon-ebs" "determinate-nixos" {

  ami_name      = "tomans-toy-image-nixos-amd64-bootstrap-staging-key"
  instance_type = "t2.micro"
  region        = var.region

  vpc_id    = var.vpc_id
  subnet_id = var.subnet_id

  source_ami_filter {
    filters = {
      architecture = "x86_64"
      root-device-type    = "ebs"
      virtualization-type = "hvm"
    }
    most_recent = true
    # https://github.com/DeterminateSystems/nixos-amis/tree/main
    owners      = ["535002876703"]
  }
  ssh_username = "root"
}

build {
  name = "tomans-toy-nixos-packer-build"
  sources = [
    "source.amazon-ebs.determinate-nixos"
  ]
  provisioner "shell" {
    environment_vars = [
    ]
    inline = [
      # "nix-shell -p 'neofetch' --run neofetch",

      # TODO: do a few extra things here
      # properly set up an initial swap device
      #
      # upgrade rolling to nixos-unstable
      # set up initial generation with earlyoom / swap configured

      # we are going to manually install a bootstrap key into this AMI
      # that means you will need that key to access this AMI!

      "rm -rf /root/.ssh",
      "mkdir -p /root/.ssh",
      "echo ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKlnymbpllMjpPPSCV4IUYMH93Uij7Vo554GITYBivvh > /root/.ssh/authorized_keys",
      "chmod 600 /root/.ssh/authorized_keys",
      "chmod 700 /root/.ssh",
      "chown -R root:root /root/.ssh"
    ]
  }
}


