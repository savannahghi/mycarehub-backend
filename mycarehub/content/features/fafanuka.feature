Feature: Fafanuka content sending

    Scenario: How do offers affect the content a subscriber receives
        Given it's the first time a subscriber joins Fafanuka
        Then they will all receive, General Information under "Diabetes General Information"
        Then after all that data is exhausted in that subgroup, they will receive content specific to a particular offer

    Scenario: How does the content states affect the content a user receives
        Given that we want to send only content that has been published
        Then when fetching content to send, we will fetch all contents where there live status == True

    Scenario: Initial content
        Given it's the first time a subscriber joins Fafanuka
        Then, they should receive the first content in "Diabetes General Information" subgroup
        When there is no content in that subgroup
        Then we don't send any content

    Scenario: Send content based on a previous sequence
        Given that the subscriber has already received previous content
        Then they will receive the next content in that sequence flow

    Scenario: Subscriber has completed the sequence in the current subgroup
        Given that the subscriber has already viewed all the content in the current subgroup
        Then we will check, if there's a next subgroup
        Then select the first content and send
