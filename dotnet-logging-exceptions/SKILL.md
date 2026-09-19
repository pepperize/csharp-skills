---
name: dotnet-logging-exceptions
description: Applies .NET logging safety and exception-boundary rules. Use when adding or reviewing `ILogger` calls, log formatting, exception throwing/catching, recoverable failures, or API error mapping. Do not use for general object design, test style, or authorization policy.
---

# .NET Logging And Exceptions

## Logging Decisions

- Log a domain-relevant failure or skip at the closest boundary that both detects or classifies it
  and owns the operational response.
- Log a failure once. Do not log and rethrow when an outer boundary will record the same failure.
- Do not hide the logging decision inside retrieval, mapping, factory, or convenience helpers.
- Extract an instance collaborator only for redaction, normalization, formatting, mapping, or
  classification.
- Keep the decision whether and at what level to log at the detection site.

## Log Safety

- Prefer omission over transformation. Log only data needed to diagnose or operate the system.
- Never log passwords, authentication or access tokens, session identifiers, API keys, encryption
  keys, connection strings, payment data, or other secrets in plaintext.
- Do not log raw request or response bodies, headers, URLs, query strings, fragments, uploaded
  content, or external-service payloads by default. Log an allow-listed summary instead.
- Treat personal data, tenant or customer identifiers, file paths, exception messages, validation
  values, and all externally supplied text as sensitive or untrusted until project policy
  explicitly classifies them as safe for the configured sink.
- Use the project's existing data-classification and redaction mechanism. If none exists, omit the
  value or ask for the required policy; do not invent a sanitizer or add a redaction package
  silently.
- Redact sensitive values. Use approved HMAC-based pseudonymization only when stable correlation
  is required. Do not use reversible encoding or an ordinary unsalted hash as redaction.
- Prefer structured `ILogger` message templates over interpolation, but pass only values already
  safe for the configured sink. Structured logging does not redact values automatically.
- When policy permits logging untrusted text, neutralize CR, LF, other control characters, and
  sink-specific delimiters, and enforce a maximum length at the final logging boundary.
- Preserve exact project-supplied safety conditions, including named delimiters and numeric length
  limits, in both recommendations and code. Do not replace them with a generic `safe...` value or
  hypothetical sanitizer. When the project says no approved mechanism exists, omit the value.
- Do not copy `Exception.Message`, response bodies, or stack traces into message-template
  arguments. Pass the exception through the `ILogger` exception overload only when the sink is
  authorized to retain its details; otherwise log a safe exception type or error code with a
  correlation identifier.
- Name extracted instance operations for their actual safety function, such as `Redact...`,
  `Normalize...`, or `CreateSafe...`. Avoid the vague term `Encode...`.
- Follow `csharp-readable-code`: do not introduce project-owned static log helpers.

## Exceptions

- Throw an exception where the problem originates.
- Do not make a helper or factory throw when its caller is the place that understands the failed invariant or boundary condition.
- Use .NET exception types whose meaning matches the failure. Do not create an application exception solely to translate malformed HTTP input.
- Map request-shape failures and client errors at the ASP.NET Core endpoint, controller, or input-adapter boundary.

## Catch Boundaries

- Do not catch broad `Exception` in orchestration code merely to log and return `null`, `false`, an empty collection, or an undifferentiated result.
- Catch only a documented or clearly owned recoverable failure that the caller can handle meaningfully.
- Let no matches in already-loaded data produce a non-null empty collection rather than an exception.
- Do not branch on human-readable exception messages or HTTP error text.
- Classify external failures with stable HTTP status, machine-readable codes, typed exceptions, or structured response fields.
- When one status code has multiple business meanings, clarify or improve the upstream contract instead of matching message text.

## Self-Review

Before finalizing:

1. Check that each log event is operationally necessary, emitted once, and remains at the failure
   or skip decision.
2. Check that every logged field is explicitly allow-listed or classified for the target sink.
3. Check that secrets are omitted and sensitive data uses the project's approved redactor.
4. Check that permitted untrusted text is control-character-safe and length-bounded.
5. Check that exception details, URLs, headers, bodies, and payloads cannot bypass the same policy.
6. Check each catch for a specific recoverable outcome owned by the caller.
7. Check that absence, empty data, and explicit results do not hide unexpected failure.
8. Check API errors are mapped at the boundary rather than expressed as domain exceptions.
