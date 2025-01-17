# Install and load necessary packages
if (!require('rvest')) install.packages('rvest')
if (!require('httr')) install.packages('httr')
install.packages("tidyverse")
install.packages("dplyr")

library(rvest)
library(httr)
library(tidyverse)
library(xml2)
library(dplyr)

print(getwd())

# FIX BING IMAGES IN A LIST
fix_urls <- function(urls_list) {

  # Remove duplicates based on 'urls' column
  for (i in seq_along(urls_list)) {
    # Apply correction and filtering function to each URL
    urls_list[[i]] <- sapply(urls_list[[i]], function(url) {
      full_url <- paste0("https://www.bing.com", url)
      return(full_url)
    })
    
  }
  
  return(urls_list)
}

# Function to get Google image URLs
get_image_urls <- function(query) {

  collected_urls <- c()
  
  while (length(collected_urls) < 30) { # Set lower limit of images per class
    url <- paste0("https://www.bing.com/images/search?q=", URLencode(query)) #paste0("https://www.google.com/search?q=", URLencode("car"))
    webpage <- read_html(GET(url, user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")))

    # Find high resolution images
    img_nodes <- html_nodes(webpage, "a[href*='/images/search?']")#html_nodes(webpage, "a[href*='/imgres?']")
    img_urls <- html_attr(img_nodes, "href")

    # Filter valid image URLs
    urls_filtrados <- img_urls[grepl("^/images/search\\?view", img_urls)]
    links_ref <- fix_urls(urls_filtrados)

    collected_urls <- unique(c(collected_urls, links_ref))

    Sys.sleep(sample(2:5, 1))
  }
  # Set upper limit of images per class
  if (length(collected_urls) > 45) {
    collected_urls <- collected_urls[1:45]
  }
  return(collected_urls)
}

# Word list
# Make sure to change between spanish and english
words <- read.csv(file.path("d:\\Internship\\WebScraper\\web_scraping_for_bing_image\\wordList.csv"), header = TRUE, fileEncoding = "Latin1")
words
spanish = words$Spanish.Gloss
spanish
image_results <- list()
for (word in spanish) {
  print(word)
  image_results[[word]] <- get_image_urls(word)
  Sys.sleep(sample(5:10, 1))
}
head(image_results)

full_image_results_df <- tibble::enframe(image_results, name = "word", value = "urls")
full_image_results_df
full_image_results_unnested <- tidyr::unnest(full_image_results_df, cols = c(urls))
full_image_results_unnested

# Remove duplicates based on 'urls' column
full_image_results_unnested_sin_duplicados <- full_image_results_unnested %>% distinct(urls, .keep_all = TRUE)
full_image_results_unnested_sin_duplicados

write.csv(full_image_results_unnested_sin_duplicados, file.path("d:\\Internship\\web_scraping_for_bing_image-main\\image_results.csv"), row.names = FALSE, fileEncoding = "Latin1")

getwd()