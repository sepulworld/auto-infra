resource "random_pet" "buddy" {
  keepers = {
    name = "walter"
  }
}

resource "random_pet" "new_buddy" {
  keepers = {
    name = "phoebe"
  }
}