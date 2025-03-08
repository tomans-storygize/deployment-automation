#!/usr/bin/env bash

# useful series of scripts for installing nix and home-manager on linux VMs

## STEP ONE: basic script checks

if [ -z "$(grep ^$(whoami): /etc/subgid)" ]; then
  echo "Missing required docker utility: https://docs.docker.com/engine/security/rootless/#prerequisites"
fi

## STEP TWO: install nix daemon

curl -sSf -L https://install.lix.systems/lix | sh -s -- install --no-confirm
. /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh


## STEP THREE: fix apparmor for rootless docker

# https://rootlesscontaine.rs/getting-started/common/apparmor/
if [ -d /etc/apparmor.d ]; then
  ROOTLESS=$(nix-shell -p rootlesskit --run 'realpath $(which rootlesskit)')
  ARMORFILE=$(echo $ROOTLESS | sed 's|/nix|nix|' | sed 's|/bin/rootlesskit||g' | tr '/' '.')
  cat <<EOT | sudo tee "/etc/apparmor.d/$ARMORFILE"
abi <abi/4.0>,
include <tunables/global>

$ROOTLESS flags=(unconfined) {
  userns,

  # Site-specific additions and overrides. See local/README for details.
  include if exists <local/$ARMORFILE>
}
EOT
  sudo systemctl restart apparmor.service
fi

## STEP FOUR: home-manager for machine user

nix-channel --add https://github.com/nix-community/home-manager/archive/master.tar.gz home-manager
nix-channel --update
nix-shell '<home-manager>' -A install

UID=$(id -u $(whoami))

cat << EndOfFile > ~/.config/home-manager/home.nix
{ config, pkgs, ... }:

{
  # Home Manager needs a bit of information about you and the paths it should
  # manage.
  home.username = "$(whoami)";
  home.homeDirectory = "${HOME}";

  # This value determines the Home Manager release that your configuration is
  # compatible with. This helps avoid breakage when a new Home Manager release
  # introduces backwards incompatible changes.
  #
  # You should not change this value, even if you update Home Manager. If you do
  # want to update the value, then make sure to first check the Home Manager
  # release notes.
  home.stateVersion = "24.11"; # Please read the comment before changing.

  # The home.packages option allows you to install Nix packages into your
  # environment.
  home.packages = [

    # # Adds the 'hello' command to your environment. It prints a friendly
    # # "Hello, world!" when run.
    pkgs.hello
    pkgs.neofetch
    pkgs.docker
    pkgs.rootlesskit
    pkgs.slirp4netns
    

    # # It is sometimes useful to fine-tune packages, for example, by applying
    # # overrides. You can do that directly here, just don't forget the
    # # parentheses. Maybe you want to install Nerd Fonts with a limited number of
    # # fonts?
    # (pkgs.nerdfonts.override { fonts = [ "FantasqueSansMono" ]; })

  ];

  # Home Manager is pretty good at managing dotfiles. The primary way to manage
  # plain files is through 'home.file'.
  home.file = {
    # # Building this configuration will create a copy of 'dotfiles/screenrc' in
    # # the Nix store. Activating the configuration will then make '~/.screenrc' a
    # # symlink to the Nix store copy.
    # ".screenrc".source = dotfiles/screenrc;

    # # You can also set the file content immediately.
    # ".gradle/gradle.properties".text = ''
    #   org.gradle.console=verbose
    #   org.gradle.daemon.idletimeout=3600000
    # '';
  };

  # Home Manager can also manage your environment variables through
  # 'home.sessionVariables'. These will be explicitly sourced when using a
  # shell provided by Home Manager. If you don't want to manage your shell
  # through Home Manager then you have to manually source 'hm-session-vars.sh'
  # located at either
  #
  #  ~/.nix-profile/etc/profile.d/hm-session-vars.sh
  #
  # or
  #
  #  ~/.local/state/nix/profiles/profile/etc/profile.d/hm-session-vars.sh
  #
  # or
  #
  #  /etc/profiles/per-user/tomans/etc/profile.d/hm-session-vars.sh
  programs.bash.enable = true;

  home.sessionVariables = {
    # EDITOR = "emacs";
    # DOCKER_HOST = "unix:///run/user/${UID}/docker.sock";
  };

  # see https://github.com/NixOS/nixpkgs/blob/master/nixos/modules/virtualisation/docker-rootless.nix

  systemd.user.services.docker = {
    Install = {
      WantedBy = [ "default.target" ];
      Description = "Docker Application Container Engine Rootless";
    };

    # needs newuidmap from pkgs.shadow
    # Path = [ "/run/wrappers" ];
    # environment = proxy_env;
  
    Unit = {
      # docker-rootless doesn't support running as root.
      ConditionUser = "!root";
      StartLimitInterval = "60s";
    };

    Service = {
      Type = "notify";
      ExecStart = "\${pkgs.writeShellScript "dockerd-rootless" ''
        #!/run/current-system/sw/bin/bash
        exec "\${pkgs.docker}/bin/dockerd-rootless"
      ''}";
      ExecReload = "\${pkgs.procps}/bin/kill -s HUP \$MAINPID";
      TimeoutSec = 0;
      RestartSec = 2;
      Restart = "always";
      StartLimitBurst = 3;
      LimitNOFILE = "infinity";
      LimitNPROC = "infinity";
      LimitCORE = "infinity";
      Delegate = true;
      NotifyAccess = "all";
      KillMode = "mixed";
    };
  }; 

  # Let Home Manager install and manage itself.
  programs.home-manager.enable = true;
}
EndOfFile

. ~/.nix-profile/etc/profile.d/hm-session-vars.sh
home-manager switch -b nixify-backup

neofetch 

## STEP FIVE: make sure docker is configured for the user

echo "waiting for rootless docker (should only take a few seconds)..."
until pids=$(pidof rootlesskit); do sleep 1; done

docker context create rootless --docker "host=unix:///run/user/${UID}/docker.sock"
docker context use rootless

docker run hello-world
