#!/bin/bash
git push origin master
ansible-playbook deployment/deploy.yml -i deployment/hosts
