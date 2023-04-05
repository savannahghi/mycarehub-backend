Feature: Fafanuka content sending

    Scenario: Content creation
        Given a content's offer, body (Swahili and English), subgroup (Facts)
        Then one should be able to create content

    Scenario: Content Workflows
        pass

    Scenario: First subscription
        Given it's the first time a subscriber joins Fafanuka
        When there is content already added added for Fafanuka
        Then they should recieve the first content, i.e under DIabetes General Information, sequence 1
        When there is no content present
        Then they should not recieve any content

    Scenario: Scheduled content
        Given a subscriber is (still) opted in to Fafanuka
        When the scheduled day and time for sending content is due
        Then they should receive published (live) content, based on their offer (TYPE1, TYPE2, GESTATIONAL, GENERAL), and the next content in their sequence
