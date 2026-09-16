// Written by infra/labs-backend/deploy.sh for the "test" stack. Safe to publish.
window.RADIANT_LAB_CONFIG = {
  stage: "test",
  region: "us-east-1",
  apiUrl: "https://ad6a0q1tsb.execute-api.us-east-1.amazonaws.com",
  userPoolId: "us-east-1_9e2tO6GgF",
  clientId: "7gs47fmifu0puf814ifjktgcdc",
  // These domains are one mailbox; sign-in folds them into the first one.
  aliasDomains: "umsystem.edu,missouri.edu,mail.missouri.edu".split(","),
};
