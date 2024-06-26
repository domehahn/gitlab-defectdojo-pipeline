#!/bin/sh

# Run playbook
ansible-galaxy collection install community.general
ansible-playbook base.yml