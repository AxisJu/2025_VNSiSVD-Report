library(tidyverse)
library(openxlsx)

df_baseline <- read.csv("Z:/2023 VNSiSVD/data/data_neuroimage_trial_processed/bids/derivatives/qsirecon/derivatives/qsirecon-DSIStudio/sub-001/ses-baseline/dwi/sub-001_ses-baseline_acq-dxi_space-ACPC_model-gqi_bundlestats.csv")[,1:40]
df_6m       <- read.csv("Z:/2023 VNSiSVD/data/data_neuroimage_trial_processed/bids/derivatives/qsirecon/derivatives/qsirecon-DSIStudio/sub-001/ses-6m/dwi/sub-001_ses-6m_acq-dxi_space-ACPC_model-gqi_bundlestats.csv")[,1:40]

df_joined <- df_baseline %>%
  rename_with(.cols = -1, .fn = ~ paste0(.x, "_baseline")) %>%
  left_join(
    df_6m %>%
      rename_with(.cols = -1, .fn = ~ paste0(.x, "_6m")),
    by = "bundle_name"
  )

metrics <- colnames(df_baseline)[-1]
list_of_sheets <- list()

for (m in metrics) {
  col_base <- paste0(m, "_baseline") 
  col_6m   <- paste0(m, "_6m")
  
  if(!all(c(col_base, col_6m) %in% colnames(df_joined))) {
    next
  }
  
  df_m <- df_joined %>%
    select(bundle_name, all_of(col_base), all_of(col_6m)) %>%
    mutate(difference = .data[[col_6m]] - .data[[col_base]]) %>%
    arrange(desc(difference))
  
  list_of_sheets[[m]] <- df_m
}

write.xlsx(
  list_of_sheets,
  file = "Z:/2023 VNSiSVD/results/20250410 DXI/statistic_dxi_250410.xlsx"
)
