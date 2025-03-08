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

source "amazon-ebs" "ubuntu" {

  ami_name      = "tomans-toy-image-ubuntu-22-amd64"
  instance_type = "t2.micro"
  region        = var.region

  vpc_id    = var.vpc_id
  subnet_id = var.subnet_id

  source_ami_filter {
    filters = {
      name                = "ubuntu/images/*ubuntu-jammy-22.04-amd64-server-*"
      root-device-type    = "ebs"
      virtualization-type = "hvm"
    }
    most_recent = true
    owners      = ["099720109477"]
  }
  ssh_username = "ubuntu"
}

build {
  name = "tomans-toy-image-packer-build"
  sources = [
    "source.amazon-ebs.ubuntu"
  ]
  provisioner "shell" {
    environment_vars = [
      "NIXIFY=https://gist.githubusercontent.com/tomans-storygize/fb9a011fb8b7d46d20dc7af82b90cdac/raw/1115e9c4a396a1c829cd5b5941414e48885efe4a/nixify.sh",
      "DEBIAN_FRONTEND=noninteractive"
    ]
    inline = [
      # upgrade to latest packages
      "sudo bash -c 'apt-get update && apt-get upgrade -y'",
      # currently requiring uidmap/dbus-user-session for rootless docker
      "sudo apt-get install dbus-user-session uidmap -y",
      # setup home-manager and rootless docker
      "curl $NIXIFY | sh -s"
    ]
  }
}


