{ config, pkgs, ... }:

{

  # modified version of docker-rootless home-manager:
  #
  #  https://gist.github.com/tomans-storygize/fb9a011fb8b7d46d20dc7af82b90cdac/raw/9eaa7883ea05e656272434332c9c2862b6e1c1b2/nixify.sh
  # 

  # Home Manager needs a bit of information about you and the paths it should
  # manage.
  home.username = "ubuntu";
  home.homeDirectory = "/home/ubuntu";

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

    pkgs.borgbackup

    # pkgs.borgbackup
    # pkgs.rsync
    
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


  programs.borgmatic = {
    enable = true;
    backups.local = let
      backupDir = "/var/lib/borgbackup/local.backup";
      sourceDirs = [
        "/var/lib/silverbullet"  
        "/var/lib/linkding"
      ];
      ensureBorgBackupRepo = "${pkgs.writeShellScript "ensure-borgrepo" ''
        #!/run/current-system/sw/bin/bash
        # this script makes sure the borgrepo is initialized before running
        BACKUP_DIR=${backupDir}

        if [ ! -d $BACKUP_DIR ]; then
          echo "Creating backup dir: $BACKUP_DIR"
          sudo mkdir -p $BACKUP_DIR
          sudo chown -R $(whoami) $BACKUP_DIR
        fi

        if [ ! -f "$BACKUP_DIR/config" ]; then
          echo "Initializing borg repo: $BACKUP_DIR"
          ${pkgs.borgbackup}/bin/borg init --encryption=none "$BACKUP_DIR"
        fi
      ''}";
    in {
      location = {
        sourceDirectories = sourceDirs;
        repositories = [ "${backupDir}" ];
      };

      retention = {
        keepHourly = 24;
        keepDaily = 7;
        keepWeekly = 4;
        keepMonthly = 6;
        # extraConfig = {
        #   prefix = "backup-";
        # };
      };

      storage = {
        extraConfig = {
          compression = "zstd";
        };
      };

      # consistency = {
      #   checks = [ "repository" "archives" ];
      # };

      hooks = {
        extraConfig = {
          before_backup = [
            ensureBorgBackupRepo
            "echo starting borg backup"
          ];
          after_backup = [
              "echo completed borg backup"
          ];
        };
      };
    };

  };

  # services.borgmatic = {
  #   # this service is requiring polkit... for systemd-inhibit perms...
  #   # so: let's not use it
  #   enable = true;
  #   frequency = "*:0/1"; # every 1 minute
  # };

  systemd.user.timers.borgmatic = {
    Timer = {
     OnCalendar = "*:0/1"; # see https://man7.org/linux/man-pages/man7/systemd.time.7.html
     Persistent = true;
     RandomizedDelaySec = "10m";
   };
   Install.WantedBy = [ "timers.target" ];
  };

  systemd.user.services.borgmatic = {
    Install = {
      WantedBy = [ "default.target" ];
      Description = "borgmatic backup timer";
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
      Type = "oneshot";
      Nice = 19;
      CPUSchedulingPolicy = "batch";
      IOSchedulingClass = "best-effort";
      IOSchedulingPriority = 7;
      IOWeight = 100;
      Restart = "no";
      LogRateLimitIntervalSec = 0;
      ExecStart = "${pkgs.writeShellScript "run-bormatic" ''
        #!/run/current-system/sw/bin/bash
        exec ${pkgs.borgmatic}/bin/borgmatic \
                 --stats \
                 --verbosity -1 \
                 --list \
                 --syslog-verbosity 1
      ''}";
    };
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
    # DOCKER_HOST = "unix:///run/user/1000/docker.sock";
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
      ExecStart = "${pkgs.writeShellScript "dockerd-rootless" ''
        #!/run/current-system/sw/bin/bash
        exec "${pkgs.docker}/bin/dockerd-rootless"
      ''}";
      ExecReload = "${pkgs.procps}/bin/kill -s HUP $MAINPID";
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
