#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)

import tempfile
from email.policy import default

__metaclass__ = type

DOCUMENTATION = r'''
---
module: s3fs

short_description: s3fs mounting buckets

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This is a module to mount buckets into filesystem

options:
    image:
        description: Image name to scan with trivy for vulnerabilities
        required: true
        type: str
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - my_namespace.my_collection.my_doc_fragment_name

author:
    - Dominik Hahn (@Devilluminati)
'''

EXAMPLES = r'''

'''

RETURN = r'''

'''

import subprocess
import os

from ansible.module_utils.basic import AnsibleModule


def getAdditionalS3fsOptions(args):
    if args:
        args_list = args.split(',')
        args_list_with_prefix = ['-o' + arg.strip() for arg in args_list]
        concatenated_args = ''.join(args_list_with_prefix)
        return concatenated_args
    else:
        return None

def getPasswdFile(module):
    bucket_value = module.params['bucket']
    access_key_id_value = module.params['accessKeyId']
    secret_access_key_value = module.params['secretAccessKey']

    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, mode='w') as tmp_file:
        tmp_file.write(f"{bucket_value}:{access_key_id_value}:{secret_access_key_value}")

    passwd_file_string = f"passwd_file={tmp_file.name}"
    return passwd_file_string

def mount_bucket(module):
    s3fs_args = getAdditionalS3fsOptions(module.params['args'])
    passwd_file = getPasswdFile(module)
    command = [
        's3fs',
        s3fs_args,
        '-o', passwd_file,
        '-o', f"url={module.params['url']}",
        module.params['bucket'],
        module.params['mount']
    ]
    subprocess.run(command, capture_output=True, text=True).stdout

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        url=dict(type='str', required=True),
        bucket=dict(type='str', required=True),
        mount=dict(type='str', required=True),
        accessKeyId=dict(type='str', required=True),
        secretAccessKey=dict(type='str', required=True),
        args=dict(type='str', required=False)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    for arg_name, arg_info in module_args.items():
        if arg_info['required'] and (module.params[arg_name] is None or module.params[arg_name] == ''):
            module.fail_json(msg=f'You need to specify a value for {arg_name}.', **result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    mount_bucket(module)

    result['message'] = 'Successfully mount bucket into folder.'
    result['changed'] = True

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()