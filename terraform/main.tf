# 1. Дефинираме Google Cloud като наш доставчик (Provider)
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# 2. Дефинираме променливи за лесна конфигурация
variable "project_id" {
  type        = string
  description = "Идентификационен номер на вашия Google Cloud проект"
  default     = "ai-os-voice-agent-web-2026"
}

variable "region" {
  type    = string
  default = "europe-west3" # Използваме Франкфурт (близо до България за минимално забавяне)
}

# 3. Ресурс за пускане на нашия Docker контейнер в Google Cloud Run
resource "google_cloud_run_v2_service" "backend" {
  name     = "ai-voice-agent-backend"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL" # Позволяваме достъп от целия свят (вкл. от телефона ти)
  
  template {
    containers {
      image = "gcr.io/${var.project_id}/backend:latest"
      
      ports {
        container_port = 8000
      }
      
      # Подаваме Gemini API Ключа като променлива на средата в Облака
      env {
        name  = "GEMINI_API_KEY"
        value = "ТВОЯТ_ОБЛАЧЕН_API_KEY"
      }
    }
  }
}

# 4. Позволяваме публичен неоторизиран достъп (всеки уеб браузър да може да си говори с бекенда ни)
resource "google_cloud_run_v2_service_iam_member" "noauth" {
  location = google_cloud_run_v2_service.backend.location
  name     = google_cloud_run_v2_service.backend.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# 5. Ресурс за активиране на базата данни Cloud Firestore за съхранение на сесиите
resource "google_firestore_database" "database" {
  name        = "(default)"
  location_id = var.region
  type        = "FIRESTORE_NATIVE"
}

# Извеждаме финалния HTTPS URL адрес в конзолата, когато всичко е готово
output "backend_url" {
  value = google_cloud_run_v2_service.backend.uri
}
