# Xinference: Overview

Xinference (Xorbits Inference) is an open-source framework for serving AI models. It
takes an open model and turns it into a running service you can call through an API,
without building the deployment plumbing yourself.

Its core purpose is to standardize and simplify model deployment so developers focus
on their application instead of underlying infrastructure. You can set up and serve a
model for experimentation or production with a single command.

It runs in the cloud, on-premises, or on a laptop. The same tool scales from a single
machine up to a distributed cluster across multiple devices, using GPUs or CPUs.

The headline value proposition is that you can swap a closed model like GPT for any
open model by changing a single line of code, because Xinference exposes one unified,
OpenAI-compatible API. Teams adopt it mainly to control cost, data privacy, and model
choice rather than depending on a closed vendor API.

It ships in two editions: a community edition that drives developer adoption, and an
enterprise platform with additional features for production-grade deployment at scale.
