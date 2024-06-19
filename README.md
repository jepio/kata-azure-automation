This repo is used by the Kata Containers CI to clean up AKS clusters that GHA
fails to delete.

Add the policy in policy.json at the subscription level. The tagName parameter
should be set to "CreatedUTC". The policy needs to be given "Tag Contributor"
permissions.

Deploy the autodelete-aks function app in the same subscription. Enable a
system-managed identity for the app and give it "Contributor" access to the
subscription.

The function app has been developed and tested with Python 3.9 in mind.

