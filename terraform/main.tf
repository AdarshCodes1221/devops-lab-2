terraform {
  required_version = ">= 1.5.0"
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
  }
}

provider "local" {}

resource "local_file" "transcoder_output" {
  filename = "${path.module}/output.end"
  content  = "transcoder engine ready\nmax_bitrate=4k\n"
}

output "transcoder_output_file" {
  description = "Path to the generated transcoder output file"
  value       = local_file.transcoder_output.filename
}
